#!/usr/bin/python
# -*- coding:UTF-8 -*-
#
# 	Copyright (C) 2019 - All Rights Reserved
# 	所属工程: ceph_test_analysis
# 	模块名称: fio_result_analysis.py
# 	创建日期: 2019/1/24 10:06
# 	代码编写: fanwen
# 	功能说明:
# 	    自动分析fio压测结果，可同时分析客户端和ceph集群
#
from io_result_deal import get_alltest_vms_iops
from io_result_deal import write_vmio_excel
from cephw_analysis import CCephwIoAnalysis
from vm_latency import CVmLatency


# 分析ceph集群结果
def AnalysisCephCluster(cephw=True, ceph_report_path=""):
    # 分析ceph集群iops及带宽，并画成曲线图
    cia = CCephwIoAnalysis(ceph_report_path, cephw)
    cia.analysis_report_files()
    cia.analysis_iops_bandwidth()


def AnalysisCephClient(client_report_path):
    # 分析ceph客户端的fio数据
    all_client_fio_data = dict()
    get_alltest_vms_iops(client_report_path, all_client_fio_data)

    # 将详细的ceph客户端延时写到excel表格中
    write_vmio_excel("%s/client_io.xls" % client_report_path, all_client_fio_data["client"])

    # 画延时图
    cvl = CVmLatency(client_report_path, all_client_fio_data)
    cvl.analysis_report_files()
    cvl.analysis_iops_latency()


# if __name__ == "__main__":
#     AnalysisCephClient("../iops_report/client/")
