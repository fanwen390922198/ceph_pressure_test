#!/usr/bin/python
# -*- coding:UTF-8 -*-

# Copyright (C) 2018 - All Rights Reserved
# 模块名称: ceph_osd_perf.py
# 创建日期: 2018/5/15
# 代码编写: fanwen
# 功能说明:
#     本程序会动态的，间隔性的将osd perf打印到屏幕，并写到日志文件中


import time
import threading
try:
    import Queue as queue
except ImportError:
    import queue


__RUN_TIME__ = 120    # 默认运行200s
__FRESH_GAP__ = 2    # 刷新频率

__HIGH_LATENCY_LINE__ = 20 # 超过20 ms就算高延时


from base_lib.szt_sys import run_cmd


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


class osd_perf_count:
    def __init__(self, osd_id, host_name):
        self.id = osd_id
        self.host = host_name
        self.apply_latency = []
        self.commit_latency = []

    def add_latency(self, apply_latency, commit_latency):
        self.apply_latency.append(apply_latency)
        self.commit_latency.append(commit_latency)

    def get_count(self):
        counts = len(self.commit_latency)     # 出现commit时延的次数
        com_max = max(self.commit_latency)
        com_min = min(self.commit_latency)
        com_ave = sum(self.commit_latency) / counts
        app_max = max(self.apply_latency)
        app_min = min(self.apply_latency)
        app_ave = sum(self.apply_latency) / counts
        return [str(self.id), str(counts), str(com_max), str(com_min), str(com_ave), str(app_max), str(app_min), str(app_ave), self.host]


class perf_count_thread(threading.Thread):
    def __init__(self, th_queue, exit, cluster):
        super(perf_count_thread, self).__init__()
        self.queue = th_queue  # 线程同步队列
        self._exit = exit
        self.cluster = cluster
        self.start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.perf_log = "./ceph_osd_perf.log"

    def run(self):
        while not self._exit.get():
            try:
                osd_perf_entry = self.queue.get(timeout=1)
                osd_id = osd_perf_entry[0]
                commit_latency = osd_perf_entry[1]
                apply_latency = osd_perf_entry[2]
                self.count_perf(osd_id, apply_latency, commit_latency)
            except:
                continue
            # time.sleep(1)

        self.show_perf_()

    def count_perf(self, osd_id, app_lat, com_lat):
        if not self.cluster.cluster_perf_count.has_key(osd_id):
            self.cluster.cluster_perf_count[osd_id] = osd_perf_count(osd_id, self.cluster.osd_2_host[osd_id])

        self.cluster.cluster_perf_count[osd_id].add_latency(app_lat, com_lat)

    def show_perf_(self):
        count_res = []
        cluster_perf_count = self.cluster.cluster_perf_count
        for value in cluster_perf_count.values():
            count_res.append(value.get_count())

        mat = ["{0[0]:8}","{0[1]:8}","{0[2]:12}","{0[3]:12}","{0[4]:12}","{0[5]:12}","{0[6]:12}","{0[7]:12}","{0[8]:12}"]
        headlinde = ["osd","count", "commit_max","commit_min","commit_avg", "apply_max","apply_min","apply_avg", "host_name"]
        ss = "".join(mat)

        line_width = 100
        line_format = '{:->%d}'%line_width
        ss_line = line_format.format("---")

        fh = open(self.perf_log, 'a+')
        # fh.write("----------------------------------------------------------------------------------------------\n")
        fh.write(ss_line + "\n")
        fh.write("script run start at: %s\n"%self.start_time)
        fh.write(ss.format(headlinde) + "\n")

        ll = sorted(count_res, key = lambda x:(x[8], eval(x[1])), reverse = True)
        if len(ll) > 0:
            pre_node = ""
            cur_node = ll[0][8]
        for l in ll:
            pre_node = cur_node
            cur_node = l[8]
            if cur_node is not pre_node:
                fh.write(ss_line + "\n")
                fh.write(ss.format(headlinde) + "\n")
                # fh.write("----------------------------------------------------------------------------------------------\n")

            fh.write(ss.format(l) + "\n")

        fh.close()


class CCephOsdPerf(threading.Thread):
    def __init__(self, tt=__RUN_TIME__, perf_file="perf.txt"):
        super(CCephOsdPerf, self).__init__()
        self.osd_perf_list = []
        self.osd_2_host = {}
        # self.__get_osd_tree()

        self.cluster_perf_count = {} # id --> osd_perf_count
        self.th_queue = queue.Queue(maxsize=10000)
        self.pc_thread_exit = CMyLockData(False)
        self.pc_th = perf_count_thread(self.th_queue, self.pc_thread_exit, self)
        self.pc_th.perf_log = perf_file
        self.run_time = tt
        # self.pc_th.start()

    def run(self):
        self.__get_osd_tree()
        self.pc_th.start()

        while self.run_time >= 0:
            self.get_osd_perf()

            time.sleep(__FRESH_GAP__)
            self.run_time -= __FRESH_GAP__

        # self.pc_thread_exit.set(True)
        self.exit()

    def get_osd_perf(self):
        self.osd_perf_list = []
        res = run_cmd("ceph osd perf", False)
        if res[0] is not 0:
            print "get ceph -v failed!"
            return False

        osd_perf_str = res[1]
        ceph_perf_list = osd_perf_str.split('\n')[1:]
        for line in ceph_perf_list:
            try:
                info = line.split()
                id = eval(info[0])
                fs_commit_latency = info[1]
                fs_apply_latency = info[2]
                host_name = self.osd_2_host[id]
                if eval(fs_apply_latency) > __HIGH_LATENCY_LINE__:
                    self.osd_perf_list.append([info[0], fs_commit_latency, fs_apply_latency, host_name])
                    self.th_queue.put([id, eval(fs_commit_latency), eval(fs_apply_latency)])

            except Exception as e:
                print e
                continue

    def __get_osd_tree(self):
        res = run_cmd("ceph osd tree|grep -E 'host [a-zA-Z]+.*[1-9]+' -A 50", False)
        if res[0] is not 0:
            print "get ceph osd tree failed!"
            return False
        ceph_osd_str = res[1]

        ceph_osd_perf_list = ceph_osd_str.split('\n')[0:]
        cur_host = None    # 当前host
        for line in ceph_osd_perf_list:
            try:
                info = line.split()
                id = eval(info[0])
                if id < 0 :  # host
                    if info[2] == "host":
                        cur_host = info[3]
                    else:
                        cur_host = None
                    continue
                else:
                    if cur_host is not None:
                        self.osd_2_host[id] = cur_host
            except:
                continue

    def exit(self):
        self.pc_thread_exit.set(True)
        self.pc_th.join()

        self.run_time = 0


