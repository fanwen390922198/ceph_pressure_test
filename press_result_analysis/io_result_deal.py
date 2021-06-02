#!/usr/bin/python
# -*- coding:UTF-8 -*-
from __future__ import division

import os
import re
import xlwt


def get_max_iops(file_path):
    f_handle = open(file_path, "r")
    done = 0
    all_iops = []
    while not done:
        one_line_log = f_handle.readline()
        if len(one_line_log) > 0:
            try:
                end = one_line_log.rfind("op/s")
                begin = one_line_log.rfind(",")
                if end > begin + 3:
                    iops = one_line_log[begin + 1: end].strip()
                    if int(iops) < 100:
                        continue
                    all_iops.append(int(iops))
            except Exception:
                print("continue")
        else:
            done = 1
    f_handle.close()

    print("MaxIOPS: ", max(all_iops), " | MinIOPS: ", min(all_iops), " | AvergIOPS:", sum(all_iops) / len(all_iops))

    # 将IOPS写入文件
    file_handle = open('IOPSDataList.txt', 'w+')
    for data in all_iops:
        file_handle.write(str(data))
        file_handle.write('\n')
    file_handle.close()

    return all_iops


# 统计io，带宽以KB/s 为单位， op 以op/s为单位
def calc_io(sd):
    d = exp_str(sd)

    # print d
    if "op/s" in d:
        return ["op", eval(d[0])]

    elif "kop/s" in d:
        return ["op", eval(d[0]) * 1000]

    else:
        if d[1] == "B/s":
            v = int(eval(d[0]) / 1000)
        elif d[1] == "MB/s":
            v = eval(d[0]) * 1000
        elif d[1] == "GB/s":
            v = eval(d[0]) * 1000 * 1000
        elif d[1] == "MiB/s":
            v = eval(d[0]) * 1024
        elif d[1] == "GiB/s":
            v = eval(d[0]) * 1024 * 1024
        elif d[1] == "KiB/s":
            v = eval(d[0]) * 1024 / 1000
        else:
            v = eval(d[0])

        return [d[-1] if len(d) > 2 else d[1], v]


def set_style(name, height, bold=False):
    style = xlwt.XFStyle()  # 初始化样式
    font = xlwt.Font()  # 为样式创建字体
    font.name = name  # 'Times New Roman'
    font.bold = bold
    font.color_index = 4
    font.height = height

    borders = xlwt.Borders()
    borders.left = 1
    borders.right = 1
    borders.top = 1
    borders.bottom = 1

    style.font = font
    style.borders = borders

    # 设置aligen
    align = xlwt.Alignment()
    align.horz = 0x02
    align.vert = 0x01
    style.alignment = align

    return style


# 使用ceph_pressure_test工具所获取的压测报告(ceph -w)
def get_ceph_w_io(cephw_file, excel_workbook=None, cephw=True):
    f_handle = open(cephw_file, "r")
    ss = f_handle.read()
    f_handle.close()
    all_io_list = []

    if excel_workbook is not None:
        row = 0
        a = os.path.split(cephw_file)
        sheet_name = os.path.splitext(a[1])[0]
        head = ["rd(kB/s)", "wr(kB/s)", "iops"]
        sheet = excel_workbook.add_sheet(sheet_name, cell_overwrite_ok=True)  # 创建sheet
        for i in range(0, len(head)):
            sheet.write(row, i, head[i], style=set_style('Times New Roman', 220, True))
        row += 1

    if cephw:
        pattern = re.compile(r'avail; (.+)')
        all_io_rec = pattern.findall(ss)
    else:
        all_io_rec = ss.split('\n')

    for rec in all_io_rec:
        io = rec.split(',')
        # print io
        try:
            io_v = [0, 0, 0]
            for s_ in io:
                [s, v] = calc_io(s_.strip())
                if s == 'rd':
                    io_v[0] = v
                elif s == 'wr':
                    io_v[1] = v
                else:
                    io_v[2] += v

            all_io_list.append(io_v)
            # print all_io_list
            if excel_workbook is not None:
                for i in range(0, len(io_v)):
                    sheet.write(row, i, io_v[i])
                row += 1
        except Exception:
            continue

    # print all_io_list

    return all_io_list


def parse_report_file_name(file):
    file_name = os.path.splitext(file)[0]
    return file_name.split('-')


def analysis_all_cephw_io(path, io_data={}, cephw=True):
    if os.listdir(path):
        all_ = os.listdir(path)
        excel_workbook = xlwt.Workbook()  # 创建工作簿

        for file in all_:
            if file.find("cephw") == -1:
                continue
            if os.path.splitext(file)[1] == '.log' or os.path.splitext(file)[1] == '.txt':

                one_file_data = get_ceph_w_io(path + file, excel_workbook, cephw)
                file_info = parse_report_file_name(file)
                # (report_type, rw_mode, size, nodes) = parse_report_file_name(file)
                rw_mode = file_info[1]
                size = file_info[2]
                nodes = ''.join(file_info[3:])

                if not io_data.has_key(rw_mode):
                    io_data[rw_mode] = {}
                if not io_data[rw_mode].has_key(size):
                    io_data[rw_mode][size] = {}

                io_data[rw_mode][size][nodes] = one_file_data

        excel_workbook.save('%scephio.xls' % path)  # 保存文件


# ----------------------------------------------------------------------#
# GetCephIo适合用压测工具所抓取到的单个虚拟机IO统计文件
# ----------------------------------------------------------------------#
def get_ceph_io(file_path):
    f_handle = open(file_path, "r")
    done = 0
    all_iops = []
    while not done:
        one_line_log = f_handle.readline()
        if len(one_line_log) > 0:
            dl = [0, 0, 0, 0]
            gdl = one_line_log.split(',')
            for s_ in gdl:
                sl_ = s_.split()
                # print (sl_)
                if sl_[1] in ["B/s", "MB/s"]:
                    if sl_[2] in ["rd"]:
                        dl[0] = eval(sl_[0])  # 读带宽
                    else:
                        dl[1] = eval(sl_[0])  # 写带宽
                elif sl_[1] in ["op/s", "kop/s", ]:
                    d = eval(sl_[0])
                    if sl_[1].find('k') != -1:
                        d = d * 1000
                    try:
                        if sl_[2] in ["rd"]:
                            dl[2] = d  # 读IOPS
                        else:
                            dl[3] = d  # 写IOPS
                    except Exception:
                        dl[2] = d  # 整个集群IO
                # print dl
                all_iops.append(dl)
        else:
            done = 1

    f_handle.close()
    return all_iops


def get_ms_float(float_data, division=3):
    if type(float_data) is int:
        return float_data

    # if float_data > 1:
    #     return int(float_data)

    ss_format = "{0:.%df}" % division

    return float(ss_format.format(float_data))


# ----------------------------------------------------------------------#
# 获取fio 压测所生成的fio报告
# ----------------------------------------------------------------------#
def get_vm_iops(file_path):
    f_handle = open(file_path, "r")
    ss = f_handle.read()
    f_handle.close()

    # pattern = re.compile(r'iops=(\d+)')
    # IOPS

    pattern = re.compile(r'IOPS=(.+),', re.I)
    iops_res = pattern.findall(ss)

    # print res
    # 统计带宽
    pattern = re.compile(r'bw=(.+)', re.I);
    bw_res = pattern.findall(ss);
    for i in range(0, len(bw_res)):
        _s = bw_res[i].replace(',', '');
        bw_res[i] = _s.split()[0]

    # print bw_res
    if len(bw_res) > 2:
        bw_res = bw_res[0:2]

    for i in range(0, len(bw_res)):
        _s = bw_res[i]
        bw_res[i] = "%d MiB/s" % (cal_bw(_s))

    # print bw_res
    # 平均延时
    # pattern = re.compile(r'clat \((\w+)\):.+avg=(\d+\.?\d+),')
    pattern = re.compile(r'clat \((\w+)\):.+avg=\s?(.+),')
    res2 = pattern.findall(ss)
    # print res2

    latency_avg = []
    for la in res2:
        # if la[0] == "msec":
        # 	latency_avg.append(str(eval(la[1])*1000))
        if la[0] == "usec":
            # latency_avg.append(str(int(eval(la[1])/1000)))
            # latency_avg.append(int(eval(la[1]) / 1000))
            latency_avg.append(get_ms_float(eval(la[1]) / 1000, 3))
        elif la[0] == "nsec":
            # latency_avg.append(int(eval(la[1]) / 1000000))
            latency_avg.append(get_ms_float(eval(la[1]) / 1000000, 6))
        else:
            latency_avg.append(get_ms_float(eval(la[1])))

    # 统计单位
    pattern = re.compile(r'clat percentiles \((\w+)\)')
    dw = pattern.findall(ss)

    # 时延分布统计
    pattern = re.compile(r'(\d+\.?\d+)th=\[\W*?(\S+).?\]')
    res3 = pattern.findall(ss)
    # print res3
    latency_interval = {
        "80": [],
        "95": []
    }
    for la in res3:
        if la[0] == '80.00':
            latency_interval["80"].append(get_ms_float(eval(la[1])))
        elif la[0] == '95.00':
            latency_interval["95"].append(get_ms_float(eval(la[1])))

    for i in range(0, len(dw)):
        # print latency_interval
        # if  dw[i] == "msec":
        # 	latency_interval["80"][i] = str(eval(latency_interval["80"][i])*1000)
        # 	latency_interval["95"][i] = str(eval(latency_interval["95"][i])*1000)
        if dw[i] == "usec":
            # latency_interval["80"][i] = int(latency_interval["80"][i] / 1000)
            latency_interval["80"][i] = get_ms_float((latency_interval["80"][i] / 1000), 3)
            latency_interval["95"][i] = get_ms_float((latency_interval["95"][i] / 1000), 3)

    for i in range(0, len(iops_res)):
        pos = iops_res[i].find('k')
        if pos != -1:
            iops_res[i] = int(eval(iops_res[i][0:pos]) * 1000)

        iops_res[i] = int(iops_res[i])

    return {"iops": iops_res,
            "bw": bw_res,
            "avg_latency": latency_avg,
            "latency_interval": latency_interval
            }


# if len(res) > 0: return eval(res[0])
# else:
#     return 0


# ---------------------------------------------------------------------#
# 适用于使用
# ---------------------------------------------------------------------#
def get_alltest_vms_iops(path, io_dict={}):
    # print path
    if not os.path.exists(path):
        print ("目录错误!")
        return
    else:
        [dir_nam, path_name] = os.path.split(path)
        if len(path_name) == 0:
            path_name = dir_nam.split('/')[-1]

    if os.path.isdir(path):
        # 列出所有子目录
        child_path_list = os.listdir(path)
        # print child_path_list
        if len(child_path_list) == 0: return

        # 查看子项是否是目录，查看第一个
        t_p = os.path.join(path, child_path_list[0])

        if os.path.isdir(t_p):  # 子项是目录
            # 给当前path添加key
            io_dict[path_name] = {}

            # 如果是目录的话，递归
            for child_path in child_path_list:
                com_child_path = os.path.join(path, child_path)
                get_alltest_vms_iops(com_child_path, io_dict[path_name])  # 递归，传入完整的子目录，空字典

        else:
            # 子项是文件
            io_dict[path_name] = []
            for child_path in child_path_list:
                com_child_path = os.path.join(path, child_path)
                vm_iops = get_vm_iops(com_child_path)
                if len(vm_iops['iops']) > 0:
                    io_dict[path_name].append(vm_iops)


def write_vmio_excel(path, vms_data={}):
    excel_workbook = xlwt.Workbook()  # 创建工作簿
    small_size_head = [
        u"读写模式", u"虚拟机数量", u"IOPS (读)", u"IOPS (写)", u"平均读时延(ms)", u"读时延80%(ms)", u"读时延95%(ms)",
        u"平均写时延(ms)", u"写时延80%(ms)", u"写时延95%(ms)"
    ]
    small_size_width = [256 * 12, 256 * 13, 256 * 13, 256 * 13, 256 * 17, 256 * 17, 256 * 17, 256 * 17, 256 * 17,
                        256 * 17]

    big_size_head = [
        u"读写模式", u"虚拟机数量", u"带宽 (读)", u"带宽(写)", u"平均读时延(ms)", u"读时延80%(ms)", u"读时延95%(ms)",
        u"平均写时延(ms)", u"写时延80%(ms)", u"写时延95%(ms)"
    ]
    big_size_width = [256 * 12, 256 * 13, 256 * 17, 256 * 17, 256 * 17, 256 * 17, 256 * 17, 256 * 17, 256 * 17,
                      256 * 17]

    style = set_style('Times New Roman', 180, True)
    for key in sorted(vms_data.keys(), key=lambda x: int(exp_str(x)[0])):
        # print key
        row = 0
        big_size = False
        sheet = excel_workbook.add_sheet(key, cell_overwrite_ok=True)  # 创建sheet
        if key in ['4k', '64k']:
            head = small_size_head
            width = small_size_width
        elif key in ['512k']:
            head = big_size_head
            width = big_size_width
            big_size = True

        for i in range(0, len(head)):
            sheet.write(row, i, head[i], set_style(u'宋体', 220, True))
            _col = sheet.col(i)
            _col.width = width[i]

        tall_style = xlwt.easyxf('font:height 500;')  # 36pt,类型小初的字号
        first_row = sheet.row(0)
        first_row.set_style(tall_style)

        row += 1

        # 遍历生成的
        size_io_data = vms_data[key]
        rw_mode_list = size_io_data.keys()
        for rw_mode in rw_mode_list:
            # print rw_mode
            rw_mode_start = row
            vms_start = row
            rw_mode_data = vms_data[key][rw_mode]
            vms_list = rw_mode_data.keys()
            for vms in sorted(vms_list):
                # print vms
                vms_iops_report = rw_mode_data[vms]

                # print vms_iops_report
                if len(vms_iops_report) == 0:
                    continue

                for i in range(0, len(vms_iops_report)):
                    if not big_size:
                        iops_report = vms_iops_report[i]['iops']
                    else:
                        iops_report = vms_iops_report[i]['bw']

                    latency_avg = vms_iops_report[i]['avg_latency']
                    latency_interval = vms_iops_report[i]['latency_interval']
                    # print latency_avg
                    # print latency_interval

                    if rw_mode == "randrw" or rw_mode == "readwrite":
                        if len(iops_report) < 2:
                            sheet.write(row, 2, "0", style)
                            sheet.write(row, 3, "0", style)
                            continue
                        sheet.write(row, 2, iops_report[0], style)
                        sheet.write(row, 3, iops_report[1], style)
                        sheet.write(row, 4, latency_avg[0], style)
                        sheet.write(row, 5, latency_interval["80"][0], style)
                        sheet.write(row, 6, latency_interval["95"][0], style)
                        sheet.write(row, 7, latency_avg[1], style)
                        sheet.write(row, 8, latency_interval["80"][1], style)
                        sheet.write(row, 9, latency_interval["95"][1], style)

                    elif rw_mode == "randwrite" or rw_mode == "write":
                        if len(iops_report) < 1:
                            sheet.write(row, 3, "0", style)
                            continue
                        sheet.write(row, 2, "", style)
                        sheet.write(row, 4, "", style)
                        sheet.write(row, 5, "", style)
                        sheet.write(row, 6, "", style)
                        sheet.write(row, 3, iops_report[0], style)
                        sheet.write(row, 7, latency_avg[0], style)
                        sheet.write(row, 8, latency_interval["80"][0], style)
                        sheet.write(row, 9, latency_interval["95"][0], style)

                    elif rw_mode == "randread" or rw_mode == "read":
                        if len(iops_report) < 1:
                            sheet.write(row, 2, "0", style)
                            continue

                        sheet.write(row, 3, "", style)
                        sheet.write(row, 7, "", style)
                        sheet.write(row, 8, "", style)
                        sheet.write(row, 9, "", style)
                        sheet.write(row, 2, iops_report[0], style)
                        sheet.write(row, 4, latency_avg[0], style)
                        sheet.write(row, 5, latency_interval["80"][0], style)
                        sheet.write(row, 6, latency_interval["95"][0], style)

                    row += 1

                sheet.write_merge(vms_start, vms_start + len(vms_iops_report) - 1, 1, 1, int(exp_str(vms)[0]),
                                  set_style('Arial', 180, False))
                vms_start = row

            if rw_mode_start < (row - 1):
                sheet.write_merge(rw_mode_start, row - 1, 0, 0, trans_mode(rw_mode), set_style(u'宋体', 180, True))

    excel_workbook.save(path)  # 保存文件


def trans_mode(rw_mode):
    mode_name = ""
    if rw_mode == "randrw":
        mode_name = u"随机读写"
    elif rw_mode == "randread":
        mode_name = u"随机读"
    elif rw_mode == "randwrite":
        mode_name = u"随机写"
    elif rw_mode == "readwrite" or rw_mode == "rw":
        mode_name = u"顺序读写"
    elif rw_mode == "read":
        mode_name = u"顺序读"
    elif rw_mode == "write":
        mode_name = u"顺序写"

    return mode_name


def cal_bw(bw):
    if len(bw) == 0:
        return 0

    res = exp_str(bw)
    if res[1] == "GiB/s":
        return int(eval(res[0]) * 1024)
    elif res[1] == "KiB/s":
        return int(eval(res[0]) / 1024)
    elif res[1] == "MiB/s":
        return int(eval(res[0]))
    elif res[1] == "KB/s":
        return int((eval(res[0]) * 1000) / (1024 * 1024))
    elif res[1] == "MB/s":
        return int((eval(res[0]) * 1000 * 1000) / (1024 * 1024))
    elif res[1] == "GB/s":
        return int((eval(res[0]) * 1000 * 1000 * 1000) / (1024 * 1024))
    else:
        return 0


def cal_vm_latency(vms_data={}):
    latency_dict = {}
    for key in sorted(vms_data.keys(), key=lambda x: int(exp_str(x)[0])):
        size_io_data = vms_data[key]
        if key not in latency_dict.keys() and len(size_io_data) > 0:
            latency_dict[key] = {}
        if len(size_io_data) == 0:
            continue

        rw_mode_list = size_io_data.keys()
        for rw_mode in rw_mode_list:
            rw_mode_data = vms_data[key][rw_mode]

            if rw_mode not in latency_dict[key].keys() and len(rw_mode_data) > 0:
                latency_dict[key][rw_mode] = {}

            if len(rw_mode_data) == 0:
                continue

            vms_list = rw_mode_data.keys()
            for vms in sorted(vms_list):
                vms_iops_report = rw_mode_data[vms]

                if len(vms_iops_report) == 0:
                    continue

                if rw_mode in ["randrw", "rw", "readwrite"]:
                    # avg_r_iops = sum([int(vm_io['iops'][0]) for vm_io in vms_iops_report]) / len(vms_iops_report)
                    avg_r_iops = sum([int(vm_io['iops'][0]) for vm_io in vms_iops_report])
                    # avg_w_iops = sum([int(vm_io['iops'][1]) for vm_io in vms_iops_report]) / len(vms_iops_report)
                    avg_w_iops = sum([int(vm_io['iops'][1]) for vm_io in vms_iops_report])
                    all_r_bw = sum([cal_bw(vm_io['bw'][0]) for vm_io in vms_iops_report])
                    all_w_bw = sum([cal_bw(vm_io['bw'][1]) for vm_io in vms_iops_report])
                    # print [vm_io['bw'][0] for vm_io in vms_iops_report]
                    # print [cal_bw(vm_io['bw'][0]) for vm_io in vms_iops_report]
                    # print all_r_bw
                    #
                    # print [vm_io['bw'][1] for vm_io in vms_iops_report]
                    # print [cal_bw(vm_io['bw'][1]) for vm_io in vms_iops_report]
                    # print all_w_bw

                    avg_r_latency = sum([vm_lat['avg_latency'][0] for vm_lat in vms_iops_report]) / len(
                        vms_iops_report)

                    avg_w_latency = sum([vm_lat['avg_latency'][1] for vm_lat in vms_iops_report]) / len(
                        vms_iops_report)

                    _vms = exp_str(vms)[0]
                    if _vms not in latency_dict[key][rw_mode].keys():
                        latency_dict[key][rw_mode][_vms] = [avg_r_iops, avg_w_iops, avg_r_latency, avg_w_latency,
                                                            all_r_bw, all_w_bw]
                    else:
                        old_data = latency_dict[key][rw_mode][_vms]
                        latency_dict[key][rw_mode][_vms] = [
                            (old_data[0] + avg_r_iops) / 2, (old_data[1] + avg_w_iops) / 2,
                            (old_data[2] + avg_r_latency) / 2, (old_data[3] + avg_w_latency) / 2,
                            (old_data[4] + all_r_bw) / 2, (old_data[5] + all_w_bw) / 2
                        ]

                if rw_mode in ["randread", "read"]:
                    # print vms_iops_report
                    # avg_r_iops = sum([int(vm_io['iops'][0]) for vm_io in vms_iops_report]) / len(vms_iops_report)
                    avg_r_iops = sum([int(vm_io['iops'][0]) for vm_io in vms_iops_report])
                    all_r_bw = sum([cal_bw(vm_io['bw'][0]) for vm_io in vms_iops_report])
                    avg_r_latency = sum([vm_lat['avg_latency'][0] for vm_lat in vms_iops_report]) / len(
                        vms_iops_report)

                    _vms = exp_str(vms)[0]
                    if _vms not in latency_dict[key][rw_mode].keys():
                        latency_dict[key][rw_mode][_vms] = [avg_r_iops, 0, avg_r_latency, 0, all_r_bw, 0]
                    else:
                        old_data = latency_dict[key][rw_mode][_vms]
                        latency_dict[key][rw_mode][_vms] = [
                            (old_data[0] + avg_r_iops) / 2, 0,
                            (old_data[2] + avg_r_latency) / 2, 0,
                            (old_data[4] + all_r_bw) / 2, 0
                        ]

                if rw_mode in ["randwrite", "write"]:
                    # print vms_iops_report
                    avg_r_iops = 0
                    # avg_w_iops = sum([int(vm_io['iops'][0]) for vm_io in vms_iops_report]) / len(vms_iops_report)
                    avg_w_iops = sum([int(vm_io['iops'][0]) for vm_io in vms_iops_report])
                    all_w_bw = sum([cal_bw(vm_io['bw'][0]) for vm_io in vms_iops_report])
                    avg_r_latency = 0
                    avg_w_latency = sum([vm_lat['avg_latency'][0] for vm_lat in vms_iops_report]) / len(
                        vms_iops_report)

                    _vms = exp_str(vms)[0]
                    if _vms not in latency_dict[key][rw_mode].keys():
                        latency_dict[key][rw_mode][_vms] = [avg_r_iops, avg_w_iops, avg_r_latency, avg_w_latency, 0,
                                                            all_w_bw]
                    else:
                        old_data = latency_dict[key][rw_mode][_vms]
                        latency_dict[key][rw_mode][_vms] = [
                            0, (old_data[1] + avg_w_iops) / 2,
                            0, (old_data[3] + avg_w_latency) / 2,
                            0, (old_data[5] + all_w_bw) / 2
                        ]
    # print latency_dict

    last_cal = {}
    # 进一步归整数据
    for key in latency_dict.keys():
        size_io_data = latency_dict[key]
        last_cal[key] = {}

        rw_mode_list = size_io_data.keys()
        for rw_mode in rw_mode_list:
            rw_mode_data = latency_dict[key][rw_mode]

            node_list = sorted(rw_mode_data.keys(), key=lambda x: int(x))
            read_iops = [rw_mode_data[nodes][0] for nodes in node_list]
            read_latency = [rw_mode_data[nodes][2] for nodes in node_list]
            write_iops = [rw_mode_data[nodes][1] for nodes in node_list]
            write_latency = [rw_mode_data[nodes][3] for nodes in node_list]

            total_read_bw = [rw_mode_data[nodes][4] for nodes in node_list]
            total_write_bw = [rw_mode_data[nodes][5] for nodes in node_list]

            last_cal[key][rw_mode] = {
                "nodes": node_list,
                "read_iops": read_iops,
                "read_latency": read_latency,
                "write_iops": write_iops,
                "write_latency": write_latency,
                "total_read_bw": total_read_bw,
                "total_write_bw": total_write_bw
            }

    return last_cal


def del_whitespace_charset(file_path):
    f_handle = open(file_path, "r+")
    all_data = f_handle.read()

    #    all_data.replace('\000','')
    new_data = ''

    # print '%X'% ord(all_data[0])

    for c in all_data:
        if c != '\000' and c != ' ' and c != '\t':
            new_data = new_data + c

    print(new_data)

    f_handle.truncate()
    f_handle.write(new_data)
    f_handle.close()


# 数据压缩
def data_compress(data_list, m=10):
    avr_list = []
    if len(data_list) < m:
        return data_list
    else:
        size = len(data_list) / m
        e = len(data_list) % m
        for i in range(0, size):
            avr_list.append(sum(data_list[i * m: (i + 1) * m]) / m)
        if e != 0:
            avr_list.append(sum(data_list[len(data_list) - e: len(data_list)]) / e)

    return avr_list


def exp_str(s):
    all_get = []
    one = ""

    for c in s:
        if c.isdigit():
            one += c

        elif c.isalpha():
            if len(one) > 0 and one[-1].isdigit():
                all_get.append(one)
                one = ""
            one += c

        elif c.isspace() or c == " ":
            if len(one) > 0:
                all_get.append(one)
                one = ""

        else:
            one += c

    if len(one) > 0:
        all_get.append(one)
    return all_get


# if __name__ == "__main__":
    # print get_ms_float(3.14159265357, 3)
    # print get_ms_float(3.14959265357, 3)
    # print get_ms_float(0.14159265357, 3)
    # print get_ms_float(3000, 3)
#     print exp_str(' 27.6MiB/s rd 8155 B/s wr ')
#     print exp_str(' 8155 B/s wr ')
#     print exp_str('3node-16th-2')
#     print exp_str('node-16th-2')
#     print exp_str('80 Mib/s')
