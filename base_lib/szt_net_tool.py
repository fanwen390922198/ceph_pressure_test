#!/usr/bin/python
# -*- coding:UTF-8 -*-
# Copyright (C) 2017 - All Rights Reserved
# 模块名称: szt_net_tool.py
# 创建日期: 2017/9/11 9:23
# 代码编写: fanwen
# 功能说明: 本模块用来检测网络连通情况

import szt_sys
import threading
import time


class CNetThread(threading.Thread):
    def __init__(self, remote_ip):
        super(CNetThread, self).__init__()
        self.ip = remote_ip
        self.__result = []     #[网络互通, ssh是否打开]

    def run(self):
        reachable = szt_sys.ping(self.ip)
        sshable = szt_sys.telnet(self.ip, 22)
        self.__result = [reachable, sshable]

    def get_result(self):
        return self.__result



# 网络检查主要检查连通性和SSH端口是否打开
class CNetTool:
    def __init__(self, remote_list):
        self.remote_list = remote_list
        self.thread_list = []
        self.is_done = False

    def check_net(self):
        for ip in self.remote_list:
            th = CNetThread(ip)
            self.thread_list.append(th)
            th.start()

        for th in self.thread_list:
            th.join()

        self.is_done = True

    def get_result(self):
        res = {}
        while not self.is_done:
            time.sleep(0.1)

        # if self.is_done:
        for th in self.thread_list:
            res[th.ip] = th.get_result()
        return res

if __name__ == "__main__":

    remote_list = ["10.10.20.181", "10.10.20.182", "10.10.20.183"]
    cnt = CNetTool(remote_list)
    cnt.check_net()
    print cnt.get_result()
