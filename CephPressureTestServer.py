#!/usr/bin/python
# -*- coding:UTF-8 -*-
# Copyright (C) 2017 - All Rights Reserved
# 模块名称: CephPressureTestServer.py
# 创建日期: 2017/12/27 11:49
# 代码编写: fanwen
# 功能说明:
#     压力测试服务端，采用C/S模式，只支持一个客户端的接入

import signal
import socket
import SocketServer
import tarfile
from base_lib.szt_log import Log
import msg_def
from pressure_test import *

gPressureTestServer = None


class PressureTestThread(threading.Thread):
    def __init__(self, pressure_test_handle, no, msg_body, log_handle):
        super(PressureTestThread, self).__init__()
        self.no = no
        self.msg = msg_body
        # self.request = request
        self.pressure_test_handle = pressure_test_handle
        self.__log_handle = log_handle

    def run(self):
        self.__log_handle.info("create fio transaction!-------->")
        param_dict = self.msg
        pt = CPressureTestTransaction(param_dict, self.__log_handle)
        pt.start_transaction()
        self.__log_handle.info("fio transaction exec complete!\r\n")

        # 返回执行结果
        self.pressure_test_handle.send_msg_to_client(self.no, msg_def.MSG_TYPE.FIO_ANS, "fio is complete!")


class PressureTestHandle(SocketServer.StreamRequestHandler):
    trans_thread_list = []

    def handle(self):
        while True:
            msg_header = msg_def.recv_all(self.request, msg_def.HEADERLEN)
            if len(msg_header) == 0:
                self.server.get_log_handler().info("%s is closed!"%(self.client_address[0]))
                break

            # 解析包头
            (no, type, body_len, has_next, expand) = msg_def.ParsePkgHeader(msg_header)

            # 获取包体
            msg_body = msg_def.recv_all(self.request, body_len)
            if len(msg_body) == 0:
                self.server.get_log_handler().info("%s is closed!"%(self.client_address[0]))
                break

            if type == msg_def.MSG_TYPE.ENGINEXIT:
                self.server.get_log_handler().info("wait all trans_thread exit!")
                self.__wait_all_trans_thread_exit()
                self.server.get_log_handler.info("PressureTestEngin exit!")
                break

            elif type == msg_def.MSG_TYPE.FIO:
                self.server.get_log_handler().info("FIO request-------->!")
                param = eval(msg_body)
                self.start_fio_transaction(no, param)

            elif type == msg_def.MSG_TYPE.FIOSTOP:
                pass

            elif type == msg_def.MSG_TYPE.HB:
                self.server.get_log_handler().info("recv heartbeat from %s" % self.client_address[0])
                self.send_msg_to_client(no, msg_def.MSG_TYPE.HB, "hb ack")

            elif type == msg_def.MSG_TYPE.FIO_REPORT:
                self.server.get_log_handler().info("FIO REPORT request-------->!")
                self.trans_fio_report(no)

            time.sleep(2)

    def send_msg_to_client(self, req_no, msg_type, msg, expand="", has_next=0):
        """
        为啥要通过次函数，只是为了更好的捕获子线程状态
        :param request:
        :param msg:
        :return:
        """
        header = msg_def.MakePkgHeader(req_no, msg_type, len(msg), has_next, expand)
        # self.server.get_log_handler().info("send to %s length:%d!" % (self.client_address[0], len(msg)))
        try:
            self.request.sendall(header + msg)
        except socket.error as e:
            self.server.get_log_handler().error(e)

    def __wait_all_trans_thread_exit(self):
        """
        等待所有的业务线程退出
        :return:
        """
        for th in self.trans_thread_list:
            th.join()

    def start_fio_transaction(self, no, param):
        th = PressureTestThread(self, no, param, self.server.get_log_handler())
        self.trans_thread_list.append(th)
        th.start()

    def trans_fio_report(self, no):
        try:
            os.remove("'client.tar.gz'")
        except:
            pass

        # 打包各个虚拟机的压测报告
        tar = tarfile.open('client.tar.gz', 'w:gz')
        try:
            for root, dir, files in os.walk('./client/'):
                for file in files:
                    fullpath = os.path.join(root, file)
                    tar.add(fullpath)
        except IOError as e:
            self.server.get_log_handler().info(str(e))

        tar.close()

        # 将压缩文件传送到客户端
        try:
            fo = open("./client.tar.gz",'rb')
            # 获取file的长度
            filelen = os.path.getsize("./client.tar.gz")
            has_next = 1

            while True:
                filedata = fo.read(4096)
                filelen -= 4096
                if not filedata:
                    break
                if filelen <= 0:
                    has_next = 0

                self.send_msg_to_client(no, msg_def.MSG_TYPE.FIO_REPORT_ANS, filedata, expand="client.tar.gz", has_next= has_next)
            fo.close()
        except Exception as e:
            self.server.get_log_handler().info(str(e))


class PressureTestEngine(SocketServer.TCPServer):
    request_queue_size = 1     # 只允许一个连接

    def __init__(self, server_address, RequestHandlerClass, log = None, bind_and_activate=True):
        """Constructor.  May be extended, do not override."""
        SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate)
        self.__log = log

    def get_log_handler(self):
        return self.__log


class CPressureTestServer:
    def __init__(self, host, port):
        """Constructor.  May be extended, do not override."""
        self.__log = Log("pressure_test", "pressure_test")
        self.__log.info("The ceph pressure test engin is started!")
        self.server = PressureTestEngine((host, port), PressureTestHandle, self.__log)
        self.thread = threading.Thread(target=self.server.serve_forever)

    def __del__(self):
        print "[info]: CPressureTestServer Destrcuting..."
        # self.__log.info("CPressureTestServer Destrcuting...")

    def run(self):
        self.thread.start()
        self.__log.info("CPressureTestServer is running")
        return True

    def stop(self):
        self.__log.info("CPressureTestServer stop")
        self.server.shutdown()

    def join(self, timeout=None):
        self.thread.join(timeout)

    def is_alive(self):
        return self.thread.isAlive()


def sig_handler(sig, frame):
    global gPressureTestServer
    if signal.SIGTERM == sig or signal.SIGINT == sig:
        gPressureTestServer.stop()
        gPressureTestServer.join()
        time.sleep(2)
        exit()


if __name__ == "__main__":
    # global gPressureTestServer
    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)

    try:
        conf = FileTool.load_json_file_dict("PressureTest.json")["Server"]
    except Exception:
        print "load conf failed!";
        exit(-1);

    gPressureTestServer = CPressureTestServer(conf["ListenIP"], conf["ListenPORT"])
    gPressureTestServer.run()

    while True:
        gPressureTestServer.join(1)
        if not gPressureTestServer.is_alive():
            break
