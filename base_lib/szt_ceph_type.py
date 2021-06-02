#!/usr/bin/python
# -*- coding:UTF-8 -*-
# 	Copyright (C) 2017 - All Rights Reserved
# 	模块名称: szt_ceph_type.py
# 	创建日期: 2017/8/25
# 	代码编写: fanwen
# 	功能说明:


class ItemType:
    osd = 0;
    host = 1;
    diskcluster = 2;
    root = - 3;
    null = -1;

    @staticmethod
    def format():
        ft = '''\
type 0 osd
type 1 host
type 2 diskcluster
type 3 root\
        ''';
        return ft;

    @staticmethod
    def get_type_name(type):
        if type == ItemType.osd:
            return "osd";
        elif type == ItemType.host:
            return "host";
        elif type == ItemType.diskcluster:
            return "diskcluster";
        elif type == ItemType.root:
            return "root";
        else:
            return "";


# ----ItemType end
class StorageType:
    ssd = "SSD"             # ssd存储设备
    sas = "SAS";            # 普通机械存储设备
    mix = "MIX";            # 混合型
    unkown = "UNKOWN";      # 位置设备


def mystrip(in_str):
    if not isinstance(in_str, str):
        return

    length = len(in_str);
    i = 0;
    for i in range(0, length):
        if in_str[i].isspace():
            i += 1
        else:
            break

    j = length - 1
    while ( j > i ):
        if in_str[j].isspace():
            j -= 1;
        else:
            break;

    return in_str[i : j + 1];
    

# if __name__ == "__main__":
#     print ItemType.format().strip();
#     print  ItemType.get_type_name(1);
#
#     print mystrip('''
#     asdasda     asdfasdf        ''');
