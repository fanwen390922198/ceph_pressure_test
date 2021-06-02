#!/usr/bin/python
# -*- coding:UTF-8 -*-
#
#     Copyright (C) 2018 - All Rights Reserved
#     所属工程: ceph_test_analysis
#     模块名称: vm_latency.py
#     创建日期: 2018/8/25 11:19
#     代码编写: fanwen
#     功能说明:
#

from io_result_deal import *
from io_chart import *

__PNG_WIDTH__ = 600
__PNG_HEIGHT__ = 400


class CVmLatency:
    def __init__(self, io_report_path, vm_client_data={}):
        self.report_path = io_report_path   # 压测报告路径
        self.vm_client_data = vm_client_data
        self.io_data = {}

    def analysis_report_files(self):
        if len(self.vm_client_data) == 0:
            get_alltest_vms_iops(self.report_path, self.vm_client_data)

        self.io_data = cal_vm_latency(self.vm_client_data['client'])

    def make_report(
                self,
                y_left_name="IOPS",
                y_right_name="latency (ms)",
                x_name="Vm numbers",
                rd_mode="read",
                size="4k",
                x_data=[],
                y_left_data=[],
                y_right_data=[]):

        c = IOChart(__PNG_WIDTH__, __PNG_HEIGHT__, "%s %s latency" % (size, rd_mode))
        c.new_data_chart()

        c.set_y_axis(y_left_name, 1, 'left', 0x2a5caa)
        c.set_y_axis(y_right_name, 1, 'right', 0xfcaf17)
        c.set_x_axis(x_data, x_name, 1)

        right_layer = c.add_layer('line', 2, 'right')
        c.add_data_set(right_layer, y_right_data, "", 0xfcaf17, 0)

        left_layer = c.add_layer('bar', 30, 'left')
        c.add_data_set(left_layer, y_left_data, "", 0x2a5caa, 3)

        print "%s%s-%s-latency.png" % (self.report_path, size, rd_mode)
        c.draw_data_chart("%s%s-%s-latency.png" % (self.report_path, size, rd_mode))

    def make_bw_report(self, rd_mode, size, x_data=[], bw_data=[]):
        c = IOChart(__PNG_WIDTH__, __PNG_HEIGHT__, "%s %s bw (Mib/s)" % (size, rd_mode))
        c.new_data_chart()

        c.set_y_axis("total bandwidth (MiB/s)", 1, 'left', 0x2a5caa)
        c.set_y_axis("", 1, 'right', 0x2a5caa)
        c.set_x_axis(x_data, "clients", 1)

        iops_layer = c.add_layer('bar', 30, 'left')
        c.add_data_set(iops_layer, bw_data, "", 0x2a5caa, 3)

        print "%s%s-%s-bandwidth.png" % (self.report_path, size, rd_mode)
        c.draw_data_chart("%s%s-%s-bandwidth.png" % (self.report_path, size, rd_mode))

    def analysis_iops_latency(self):
        for size in self.io_data.keys():
            wr_mode_list = self.io_data[size].keys()
            for mode in wr_mode_list:
                y_left_name = "IOPS"
                y_left_data_read = self.io_data[size][mode]["read_iops"]
                y_left_data_write = self.io_data[size][mode]["write_iops"]
                if size in ['512k']:
                    y_left_name = "total bandwidth (MiB/s)"
                    y_left_data_read = self.io_data[size][mode]["total_read_bw"]
                    y_left_data_write = self.io_data[size][mode]["total_write_bw"]

                self.make_report(
                    y_left_name=y_left_name,
                    y_right_name="latency (ms)",
                    x_name="vm numbers",
                    rd_mode="read",
                    size=size,
                    x_data=self.io_data[size][mode]["nodes"],
                    y_left_data=y_left_data_read,
                    y_right_data=self.io_data[size][mode]["read_latency"])

                self.make_report(
                    y_left_name=y_left_name,
                    y_right_name="latency (ms)",
                    x_name="vm numbers",
                    rd_mode="write",
                    size=size,
                    x_data=self.io_data[size][mode]["nodes"],
                    y_left_data=y_left_data_write,
                    y_right_data=self.io_data[size][mode]["write_latency"])
