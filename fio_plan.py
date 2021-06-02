#!/usr/bin/python
# -*- coding:UTF-8 -*-
#
# Copyright (C) 2017 - All Rights Reserved
# 模块名称: fio_plan.py
# 创建日期: 2018/8/7 16:15
# 代码编写: fanwen
# 功能说明:
#


class FioPlan:
    def __init__(self, ioengine="sync", pt_disk="", pool="", rbdname="", report=""):
        self.ioengine = ioengine           # {sync, libaio, rbd}

        if self.ioengine == "rbd":          # rbd块测试
            self.pool = pool               # ceph pool
            self.rbdname = rbdname         # ceph volume name
        else:
            self.pt_disk = pt_disk         # 待压磁盘

        # self.iodepth = 32                  # io深度
        self.iodepth = 16                  # io深度        
        self.pt_mode = "randrw"            # 压测模式{顺序读：read，顺序写：write, 随机读：randread, 随机写: randwrite\
                                           # 顺序混合读写: rw, readwrite, 随机混合读写：randrw}
        self.block_size = "4k"             # 读写入块大小
        self.size = "100G"                 # 总的读写入大小
        self.numjobs = 16                  # job数量
        self.runtime = 600                 # 运行时间
        self.rwmixread = 70                # 混合模式用读所占比例

        if len(report) == 0:
            self.report = "/root/fio/fio_report.txt"
        else:
            self.report = report

    def set_param(self, rw, bs, tn, rt=600, size="100G", mr=0, iodepth=32):
        self.pt_mode = rw
        self.block_size = bs
        self.size = size
        self.numjobs = tn
        self.runtime = rt
        self.rwmixread = mr
        self.iodepth = iodepth

    def make_cmd(self):
        cmd = "fio -thread -group_reporting"
        cmd += " -name=%s-%s-%d"%(self.pt_mode, self.block_size, self.numjobs)
        cmd += " -direct=1"
        cmd += " -iodepth=%d"%self.iodepth
        cmd += " -rw=%s"%self.pt_mode
        if self.pt_mode in ["rw","readwrite","randrw"]:
            cmd += " -rwmixread=%d"%self.rwmixread
        cmd += " -bs=%s"%self.block_size
        cmd += " -size=%s"%self.size
        cmd += " -numjobs=%d"%self.numjobs
        cmd += " -runtime=%d"%self.runtime
        cmd += " -ioengine=%s"%self.ioengine
    
        if self.ioengine == "rbd":
            cmd += " -pool=%s" % self.pool
            cmd += " -rbdname=%s" % self.rbdname
    
        else:
            cmd += " -filename=/dev/%s"%self.pt_disk
    
        cmd += " >> %s"%self.report
    
        # print cmd
        return cmd
