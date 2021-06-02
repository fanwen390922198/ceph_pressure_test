#!/usr/bin/python
# -*- coding:UTF-8 -*-
# Copyright (C) 2017 - All Rights Reserved
# 模块名称: pressure_test.py
# 创建日期: 2017/12/24 12:21
# 代码编写: fanwen
# 功能说明:

import os
import shutil
import threading
import time

from fio_plan import FioPlan
from base_lib.bat_operate_tool import CBatOperate
from base_lib.szt_load_conf import FileTool

REPORT_PATH = "/root/fio/"


# ceph 压力测试线程
class CephIoTestThread(threading.Thread):
    def __init__(self, node , ioengine="sync", target=None, bat_op=None):
        super(CephIoTestThread, self).__init__()
        self.node = node                   # 运行节点
        self.ioengine = ioengine
        if self.ioengine == "rbd":
            self.pool = target[0]
            self.rbd_volume = target[1]
            self.fio_plan = FioPlan(ioengine="rbd", pool=target[0], rbdname=target[1],
                                    report="/root/fio/fio_report_{}.txt".format(self.getName()))
        else:
            self.fio_plan = FioPlan(ioengine=ioengine, pt_disk=target)
        self.bat_op = bat_op
        self.report_file = "/root/fio/fio_report_{}.txt".format(self.getName())

    def set_param(self, rw, bs, tn, rt=600, size="100G", mr=70, iodepth=32):
        self.fio_plan.set_param(rw, bs, tn, rt, size, mr, iodepth)
        self.report_file = "fio-%s-%s-%s-%s.txt" % (rw, bs, self.node, self.getName())
        self.fio_plan.report = REPORT_PATH + self.report_file

    def run(self):
        cmd = self.fio_plan.make_cmd()
        self.bat_op.run_cmd_on_one_remote(self.node, "mkdir -p %s" % REPORT_PATH)

        # 执行fio命令
        self.bat_op.run_cmd_on_one_remote(self.node, cmd)

        # wait 1 sec
        time.sleep(1)
        self.bat_op.bat_copy_file_from_remote2(self.node, self.fio_plan.report, "./" + self.report_file)

        # del last report
        self.bat_op.run_cmd_on_one_remote(self.node, "rm -fr %s" % self.fio_plan.report)


class CephPressureTest:
    def __init__(self, node_list, fio_target_list, fio_param):
        self.node_list = node_list             # 节点列表
        self.fio_target_list = fio_target_list # fio压测目标列表 对rbd测试来说是volume列表，对虚拟机来说是对应的磁盘列表
        self.pressure_test_thread_list = []    # 压力测试线程集
        self.node_pt_instance = []             # 当前运行OneNodeRbdClients压力测试的vm实例
        self.fio_param = fio_param
        self.fio_engine = fio_param["engine"]
        self.bat_op = CBatOperate()        # 批处理工具
        self.fio_report = "fio-%s-%s.txt" % (self.fio_param["rw"], self.fio_param["bs"])
        self.volume_list = []
        self.pool = "rbd"
        self.every_rbd_volume_size = 1024 # 1G
        self.one_node_clients = 1
        self.all_thread_report = []
        try:
            self.conf = FileTool.load_json_file_dict("PressureTest.json")["Server"]
            self.pool = self.conf["RbdPool"]
            self.every_rbd_volume_size = self.conf["EveryRbdTestVolumeSize"]
            self.one_node_clients = self.conf["OneNodeRbdClients"]
        except Exception:
            pass

    def format_vm_disk(self):
        # 先对待压的盘格式化
        for i in range(0, len(self.node_list)):
            self.bat_op.run_cmd_on_one_remote(self.node_list[i], "mkfs.xfs -f -s size=1024 /dev/%s" %
                                              self.fio_target_list[i])

    # 启动多个节点
    def start_node_test(self, node_num):
        total_num = len(self.node_list)
        if node_num > total_num:
            node_num = total_num

        self.pressure_test_thread_list = []

        # 如果ioengine是RBD, 先创建rbd卷
        if self.fio_engine == "rbd":
            for i in range(0, node_num*self.one_node_clients):
                rbd_volume = "rbd_test_%d" % i
                self.volume_list.append(rbd_volume)
                res = self.bat_op.run_cmd_on_one_remote(self.node_list[0], "rbd list --pool %s|grep %s" %
                                                        (self.pool, rbd_volume))
                if res[0] != 0:
                    print "rbd create %s --size %s  -p %s" % (rbd_volume, self.every_rbd_volume_size, self.pool)
                    self.bat_op.run_cmd_on_one_remote(self.node_list[0], "rbd create %s --size %s  -p %s"
                                                      % (rbd_volume, self.every_rbd_volume_size, self.pool))
        else:
            self.volume_list = self.fio_target_list

        # 创建压力实例
        index = 0

        for i in range(0, node_num):
            for j in range(0, self.one_node_clients):
                th = CephIoTestThread(node=self.node_list[i], ioengine=self.fio_engine,
                                      target=[self.pool, self.volume_list[index]] if self.fio_engine == "rbd" else
                                      self.volume_list[index],
                                      bat_op=self.bat_op)
                index += 1
                th.set_param(self.fio_param["rw"], self.fio_param["bs"], self.fio_param["tn"],
                             rt=self.fio_param["rt"], size=self.fio_param["size"], iodepth=self.fio_param["iodepth"])

                self.pressure_test_thread_list.append(th)
                self.all_thread_report.append(th.report_file)

        # 启动运行实例
        print "Current Time: %s"%(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        for th in self.pressure_test_thread_list:
            th.start()

        # 等待各个运行实例退出
        for th in self.pressure_test_thread_list:
            th.join()
        
        # 如果ioengine是RBD, 删除测试过rbd设备
        # if self.fio_engine == "rbd":
        #     for i in range(0, node_num*self.one_node_clients):

        #     # for [pool, rbd_volume] in self.fio_target_list:
        #     # res = self.bat_op.run_cmd_on_one_remote(self.node, "rbd list --pool %s|grep %s"%(self.pool, self.rbd_volume))
        #     # if res[0] <> 0:
        #         print "[info]: rbd rm %s -p %s" % (self.volume_list[i], self.pool)
        #         self.bat_op.run_cmd_on_one_remote(self.node_list[0], "rbd rm %s -p %s"%(self.volume_list[i], self.pool))


class CPressureTestTransaction:
    """
    压测事务
    """
    def __init__(self, param_dict, log_handle):
        """
        :param param_dict: 参数字典
        :param log_handle: 日志句柄
        """
        self.param_dict = param_dict
        self.engine = param_dict["engine"]
        self.rw = param_dict["rw"]
        self.bs = param_dict["bs"]
        self.tn = param_dict["tn"]
        self.node_list = param_dict["node_list"]
        self.fio_target_list = param_dict["fio_target_list"]
        self.__log_handle = log_handle

        self.cpt = CephPressureTest(self.node_list, self.fio_target_list, param_dict)

    def start_transaction(self):
        # if self.rw in ["write", "randwrite", "rw", "readwrite", "randrw"] and self.engine is not "rbd":
        #     # 格式化待压虚拟机的待压磁盘
        #     self.__log_handle.info("format disk------>")
        #     self.cpt.format_vm_disk()

        # 创建压测实例进行压测
        self.__log_handle.info("start pressure test------>")
        self.cpt.start_node_test(len(self.node_list))
        self.__log_handle.info("end pressure test")

        try:
            dir_name = "%dnode-%dth-" % (len(self.node_list), self.tn)
            report_put_path = "./client/%s/%s" % (self.bs, self.rw)

            if not os.path.exists(report_put_path):   # 如果父目录不存在，则创建
                os.makedirs(report_put_path)

            no = 1
            all_child = os.listdir(report_put_path)  # 遍历父目录
            cur_vm_test = sorted([i for i in all_child if i.find(dir_name) != -1])
            if len(cur_vm_test) > 0:
                last_vm_report = cur_vm_test[-1]
                no = int(last_vm_report.split('-')[-1]) + 1

            report_put_path = report_put_path + '/' + dir_name + str(no)  # 创建报告目录
            os.mkdir(report_put_path)

            all_ = os.listdir("./")  # 将报告移到刚刚创建的目录
            for f in all_:
                fp = os.path.join("./", f)
                if f in self.cpt.all_thread_report:
                    shutil.move(fp, report_put_path)
        except Exception as e:
            self.__log_handle.info(str(e.message))
