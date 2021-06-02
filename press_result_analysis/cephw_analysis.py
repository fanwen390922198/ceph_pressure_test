#!/usr/bin/python
# -*- coding:UTF-8 -*-
#
#     Copyright (C) 2018 - All Rights Reserved
#     所属工程: ceph_test_analysis
#     模块名称: cephw_analysis.py
#     创建日期: 2018/8/25 11:19
#     代码编写: fanwen
#     功能说明:
#

from io_result_deal import *
from io_chart import *

__RBD_LIST__ = [0x009900, 0xff0000, 0x000000, 0xccff00, 0x3300cc, 0x660000, 0xcc00cc, 0xff33cc,
                0x408080, 0x9f4d95]

__PNG_WIDTH__ = 1250
__PNG_HEIGHT__ = 600


class CCephwIoAnalysis:
    def __init__(self, io_report_path, iops_from_cephw = True):
        self.report_path = io_report_path   # 压测报告路径
        self.io_data = {}
        self.iops_from_cephw = iops_from_cephw

    def analysis_report_files(self):
        analysis_all_cephw_io(self.report_path, self.io_data, cephw=self.iops_from_cephw)
        self.rd_mode_keys = self.io_data.keys()

    def make_report(self, rd_mode, size, data_dict, data_type = "iops"):
        """
        :param rd_mode:  读写模式
        :param size:     块大小
        :param data_dict:  数据集
        :param data_type: 数据类型 iops, write_bandwidth, read_bandwidth
        :return:
        """
        if data_type == "iops":
            index = 2
        elif data_type == "write_bandwidth":
            index = 1
        else:
            index = 0

        print data_type
        c = IOChart(__PNG_WIDTH__, __PNG_HEIGHT__, "ceph test: %s(%s)"%(rd_mode, size))
        c.new_data_chart()
        if data_type <> "iops":
            c.set_y_axis("KB/S", 0)
        else:
            c.set_y_axis(data_type.upper(), 0)
        c.set_x_axis([], "time --->", 1)
        layer = c.add_layer("line", 2)

        nodes_list = sorted(data_dict.keys())
        # print data_dict[nodes_list[0]]
        # nod = sorted([int(node[0:-1]) for node in nodes_list])

        for i in range(0, len(nodes_list)):
            avr_list = [d[index] for d in data_dict[nodes_list[i]]]
            c.add_data_set(layer, avr_list, nodes_list[i], __RBD_LIST__[i], 1)
            # c.chart.addTrendLayer(avr_list, __RBD_LIST__[i], "").setLineWidth(2)

        print "%s%s-%s-%s.png"%(self.report_path, rd_mode, size, data_type)
        c.draw_data_chart("%s%s-%s-%s.png"%(self.report_path, rd_mode, size, data_type))

    def analysis_iops_bandwidth(self):
        for rd_mode in self.rd_mode_keys:
            size_list = self.io_data[rd_mode].keys()
            for size in size_list:
                self.make_report(rd_mode, size, self.io_data[rd_mode][size], "iops")
                self.make_report(rd_mode, size, self.io_data[rd_mode][size], "write_bandwidth")
                self.make_report(rd_mode, size, self.io_data[rd_mode][size], "read_bandwidth")


# if __name__ == "__main__":
#     cia = CCephwIoAnalysis("./chuangjin/vm/ceph/")
#     cia.analysis_report_files()
#     cia.analysis_iops_bandwidth()