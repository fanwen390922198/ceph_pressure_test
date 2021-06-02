#!/usr/bin/python
# -*- coding:UTF-8 -*-
# Copyright (C) 2017 - All Rights Reserved
# 模块名称: CephPressureTestClient.py
# 创建日期: 2018/1/5 9:50
# 代码编写: fanwen
# 功能说明: 压力测试客户端

import shutil
import threading
import time
import socket
import os
import tarfile

import msg_def
from ceph_io import CephwThread
from base_lib.szt_load_conf import FileTool
from base_lib.szt_log import Log

from base_lib.daemonize import daemonize

from press_result_analysis.FioResultAnalysis import *

# 时间间隔(S) 获取CEPH集群状态的定时器
TIMEGAP = 3

# 心跳包间隔
HBGAP = 6

# 当一个fio跑完，下一个fio启动的中间间隔(这是为了防止ceph io并未全部完成)
WAIT_CEPHIO_COMPLETE = 10


# 多线程同步
class CMyLockData:
    def __init__(self, data):
        self.d = data
        self.mutex = threading.Lock()    # 创建互斥锁

    def get(self):
        self.mutex.acquire()
        d = self.d
        self.mutex.release()
        return d

    def set(self, data):
        self.mutex.acquire()
        self.d = data
        self.mutex.release()


# 心跳线程
class CHBThread(threading.Thread):
    def __init__(self, socket, is_exit):
        super(CHBThread, self).__init__()
        self.socket = socket
        self.is_exit = is_exit

    def run(self):
        while not self.is_exit.get():
            header = msg_def.MakePkgHeader(0, msg_def.MSG_TYPE.HB, len("heart beat"))
            try:
                self.socket.sendall(header + "heart beat")
            except Exception:
                pass

            time.sleep(HBGAP)


# 消息接收线程
class CRecvThread(threading.Thread):
    def __init__(self, socket, parent):
        super(CRecvThread, self).__init__()
        self.sock = socket
        self.parent = parent
        self.is_exit = parent.HB_thread_exit
        self.fio_event = parent.fio_complete_event
        self.log = parent.log

    def run(self):
        while not self.is_exit.get():
            msg_header = msg_def.recv_all(self.sock, msg_def.HEADERLEN)
            if len(msg_header) == 0:
                break
            # 解析包头
            (no, type, body_len, has_next, expand) = msg_def.ParsePkgHeader(msg_header)
            # print no, type, body_len, has_next, expand

            # 获取包体
            msg_body = msg_def.recv_all(self.sock, body_len)

            if body_len > 0 and len(msg_body) == 0 :
                break

            # 路由消息类型
            if type == msg_def.MSG_TYPE.HB:     # 心跳
                self.log.info("recv hb_ack from server")

            elif type == msg_def.MSG_TYPE.FIO_REPORT_ANS:   # 压测报告应答
                vm_fio_report_name = expand.replace("\x00", "")

                if len(self.parent.vm_fio_report_name) == 0:
                    self.parent.vm_fio_report_name = vm_fio_report_name

                fp = open(vm_fio_report_name, "ab")  # 以追加的方式写入
                fp.write(msg_body)
                fp.close()

            elif type == msg_def.MSG_TYPE.FIO_ANS:  # fio任务完成应答
                self.fio_event.set()

            if has_next is not 0:  # 后端业务分包了
                continue
            else:
                if type == msg_def.MSG_TYPE.FIO_REPORT_ANS:
                    self.parent.fio_report_semaphore.release()

            time.sleep(1)


# ----------------------------------------------------#
#    ceph 自动化测试引擎
# ----------------------------------------------------#
class CephPressureTestControl:
    def __init__(self, log, conf={}):
        self.log = log
        self.conf = conf
        self.node_list = self.conf["ClientList"]
        self.fio_target_list = self.conf["ClientPressTestTarget"]
        self.pkg_no = 0
        self.vm_fio_report_name = ""
        self.all_report_dir = "./iops_report"
        self.HB_thread_exit = CMyLockData(False)
        self.fio_complete_event = threading.Event()         # fio 完成事件
        self.fio_report_semaphore = threading.Semaphore(1)  #
        self.fio_report_semaphore.acquire()
        self.HB_thread = None
        self.RC_thread = None
        # self.Cephw_thread = None
        self.sock = None
        self.cephw = True if self.conf["CephIO"] is "ceph -w" else False

    def __del__(self):
        if not self.HB_thread_exit.get():
            self.HB_thread_exit.set(True)

        self.HB_thread.join()

        if self.RC_thread is not None:
            self.RC_thread.join()

        print "shutdown socket"
        self.sock.close()

    def fio_finished(self):
        if not self.HB_thread_exit.get():
            self.log.info("set exit signals!")
            self.HB_thread_exit.set(True)

        self.HB_thread.join()

        if self.RC_thread is not None:
            self.RC_thread.join()

        self.log.info("shutdown socket")
        self.sock.close()

    def init_communicate(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((self.conf["PressureTestServer"], self.conf["PressureTestPort"]))
        except Exception:
            self.log.error("connect to engine failed!")
            exit(-1)

        # 开始发心跳包
        self.HB_thread = CHBThread(self.sock, self.HB_thread_exit)
        self.HB_thread.start()

        # 开始通信
        self.RC_thread = CRecvThread(self.sock, self)
        self.RC_thread.start()

    def make_transaction_param(self, rw, bs, rt, tn, iodepth, nodes, fio_targets, size="100G"):
        param_dict = dict()
        param_dict["engine"] = self.conf["FioEngine"]
        param_dict["rw"] = rw   # 读写模式
        param_dict["bs"] = bs   # 读写块大小
        param_dict["tn"] = tn
        param_dict["rt"] = rt
        param_dict["size"] = size
        param_dict["iodepth"] = iodepth

        param_dict["node_list"] = nodes
        param_dict["fio_target_list"] = fio_targets

        return str(param_dict)
        # return str(param_dict).replace('\'','\\\"')

    def __get_report(self):
        header = msg_def.MakePkgHeader(self.pkg_no, msg_def.MSG_TYPE.FIO_REPORT, len("fio_report"))
        self.pkg_no += 1
        self.sock.sendall(header + "fio_report")

    def run_one_transaction(self, rw="randwrite", bs="4k", tn=10, iodepth=32, tms=600, vms=[], vmds=[], size="100G"):
        # 启动压测程序
        param = self.make_transaction_param(rw, bs, tms, tn, iodepth, vms, vmds, size)
        msg_header = msg_def.MakePkgHeader(self.pkg_no, msg_def.MSG_TYPE.FIO, len(param))
        self.pkg_no += 1
        self.sock.sendall(msg_header + param)

        if self.conf["IsCephPressTest"] != 0:
            # 获取集群状态
            th = CephwThread(tt=tms, report="./cephw-%s-%s-%sclient.txt" % (rw, bs, len(vms)),
                             perf_report="./perf-%s-%s-%sclient.txt" % (rw, bs, len(vms)),
                             cephw=self.cephw)
            th.start()
            return th
        else:
            return None

    def regular_fio_report(self):
        if not os.path.exists("%s/ceph/" % self.all_report_dir):
            os.makedirs("%s/ceph/" % self.all_report_dir)

        try:
            all_ = os.listdir("./")
            all_report_txt = [f for f in all_ if os.path.splitext(f)[1] == '.txt']
            for f_txt in all_report_txt:
                fp = os.path.join("./", f_txt)
                fn = os.path.splitext(f_txt)[0]
                all_had_report = os.listdir(self.all_report_dir + '/ceph/')
                same_report = [f for f in all_had_report if os.path.splitext(f)[0].find(fn) is not -1]
                i = len(same_report)
                shutil.move(fp, "%s/ceph/%s" % (self.all_report_dir, fn + '-' + str(i+1) + '.txt'))

        except Exception as e:
            print str(e)

        try:
            self.__get_report()

            self.fio_report_semaphore.acquire()   # 等待报告传输完成信号

            if os.path.exists("%s/%s" % (self.all_report_dir, self.vm_fio_report_name)):
                os.remove("%s/%s" % (self.all_report_dir, self.vm_fio_report_name))
            shutil.move(self.vm_fio_report_name, self.all_report_dir)

            tar = tarfile.open("%s/%s" % (self.all_report_dir, self.vm_fio_report_name), "r:gz")
            tar.extractall(self.all_report_dir)
            tar.close()
            os.remove("%s/%s" % (self.all_report_dir, self.vm_fio_report_name))

        except Exception as e:
            print str(e)

    def run(self):
        fio_plan = self.conf["FioPlan"]

        for plan in fio_plan:
            t_nam = "wr: {}, blk: {}, size: {}, th: {}, iodepth: {}, time: {}(s), clients: {}".format( \
                    plan["rw_type"], plan["block_size"], plan["total_size"], plan["numjobs"], \
                    plan["iodepth"], plan["run_time"], plan["client_nums"])

            self.log.info("engine: %s, %s"%(self.conf["FioEngine"], t_nam))

            th = self.run_one_transaction(rw=plan["rw_type"], bs=plan["block_size"], tn=plan["numjobs"], \
                                          iodepth=plan["iodepth"], tms=plan["run_time"], size=plan["total_size"], \
                                          vms=self.node_list[0:plan["client_nums"]], \
                                          vmds=self.fio_target_list[0:plan["client_nums"]])

            self.fio_complete_event.clear()

            # 等待fio事务完成
            self.fio_complete_event.wait(plan["run_time"]*2)

            time.sleep(WAIT_CEPHIO_COMPLETE)

            if th is not None:
                if th.isAlive():
                    th.exit()
                th.join()

            # 等待一会儿再做下一个测试
            time.sleep(60)

        self.log.info("get fio report!")
        self.regular_fio_report()

        self.log.info("fio finished!")
        self.fio_finished()

        # 分析结果
        self.log.info("analysis presstest result!")
        if self.conf["IsCephPressTest"] != 0:
            AnalysisCephCluster(False, "./iops_report/ceph/")

        AnalysisCephClient("./iops_report/client/")


def main(log, press_test_conf):
    ct = CephPressureTestControl(log, press_test_conf)
    ct.init_communicate()
    ct.run()

    log.info("end pressure test!");
    return 0;


if __name__ == "__main__":
    log = Log("press_test_client", "press_test_client");
    log.info("start pressure test!");

    try:
        press_test_conf = FileTool.load_json_file_dict("PressureTest.json")["Client"]
    except Exception:
        log.error("load conf failed!")
        exit(-1)

    if "Daemon" in press_test_conf and press_test_conf["Daemon"] == 1:
        daemonize('/dev/null', '/tmp/press_test_client.log', '/tmp/press_test_client_err.log')

    exit(main(log, press_test_conf))


