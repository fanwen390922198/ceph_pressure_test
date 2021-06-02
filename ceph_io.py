#!/usr/bin/python
# -*- coding:UTF-8 -*-

# Copyright (C) 2018 - All Rights Reserved
# 模块名称: ceph_io.py
# 创建日期: 2018/8/7
# 代码编写: fanwen
# 功能说明:

import threading
import re
import time,datetime
import subprocess
import os
import signal
import warnings
from base_lib.szt_sys import run_cmd

from ceph_osd_perf import CCephOsdPerf


TIMEGAP = 1
TIME_FOR_EXIT = 15

CEPH_VERSION_LUMIOUS = "client:"


# -----------------------------------------------------------------------------#
# 通过ceph -s 获取集群性能
# -----------------------------------------------------------------------------#
def GetCephIoStatus(tt, report):
    c = 0
    ceph_idel_time = TIME_FOR_EXIT

    print "[info]: start a thread to get ceph io to %s!\n"%report
    fd = open(report, "a+")

    while(c < tt):
        res = run_cmd("ceph -s", False)
        if (res[0] == 0):
            status = res[1]
            # pattern = re.compile(r'client io (.+)')
            pattern = re.compile(r'client:(.+)')
            str_io = pattern.findall(status)
            if len(str_io) > 0:
                # print str_io[0].strip()
                fd.write(str_io[0].strip() + '\r\n')
                ceph_idel_time = TIME_FOR_EXIT     # 若有io过来，重新统计空闲

            else:   # -- 此时ceph -s 没有返回系统IO，表明系统无压力
                ceph_idel_time -= TIMEGAP
                if ceph_idel_time <= 0:
                    print "[error]: the ceph cluster is idel for %d secs!"%TIME_FOR_EXIT
                    break     #-- 连续空闲之间超过，TIME_FOR_EXIT
        else:
            print "[error]: get ceph status failed!"
            break  # -- 获取失败

        c += TIMEGAP
        time.sleep(TIMEGAP)

    fd.close()
    print "[info]: thread exit!"
    return 0


def stop_subprocess(*args, **kwargs):
    print "[info]: stop subprocess at：", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    parent = args[0]
    parent.clear_sub()


# -----------------------------------------------------------------------------#
# 通过ceph -w 获取集群性能
# -----------------------------------------------------------------------------#
class CephwThread(threading.Thread):
    def __init__(self, tt, report= "cephw.txt", perf_report = "", cephw = False):
        super(CephwThread, self).__init__()
        self.tt = tt  # 运行时间
        self.report = report
        self.perf_report = perf_report
        self.cephw = cephw
        self.sub = None
        self.timer = None
        self.osd_perf_thread = None   # 获取osd性能的线程

    def run(self):
        print "[info]: start subprocess at：", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        # 先开启获取集群性能的线程
        self.osd_perf_thread = CCephOsdPerf(self.tt, self.perf_report)
        self.osd_perf_thread.start()

        if not self.cephw:
            GetCephIoStatus(self.tt, self.report)
        else:
            # 使用一个定时器去关闭子进程
            self.timer = threading.Timer(self.tt, stop_subprocess, [self])
            self.timer.start()

            self.sub = subprocess.Popen("ceph -w > %s"%self.report, shell=True, preexec_fn=os.setsid)
            self.sub.wait()

            self.timer.join()

        self.osd_perf_thread.join()

    def clear_sub(self):
        self.osd_perf_thread.exit()

        self.sub.terminate()
        self.sub.wait()

        try:
            os.killpg(self.sub.pid, signal.SIGTERM)
        except OSError as e:
            warnings.warn(e)

    def exit(self):
        self.osd_perf_thread.exit()

        if self.cephw:
            # 先关闭子进程
            self.clear_sub()

            # 主动关闭定时器，也请主动关闭子进程
            self.timer.cancel()
            self.timer.join()


# if __name__ == "__main__":
#     GetCephIoStatus(30,'./test_cephw.log')
