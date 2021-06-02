#!/usr/bin/python
# -*- coding:UTF-8 -*-
# Copyright (C) 2017 - All Rights Reserved
# 模块名称: szt_ceph_type.py
# 创建日期: 2017/8/25
# 代码编写: fanwen
# 功能说明: 本文件主要时间json文件加载和crushmap文件加载


import json
import types


class JsonNotDictException(Exception):
    def __init__(self):
        super(JsonNotDictException, self).__init__(self, "your file is not json file!")


class FileNullException(Exception):
    def __init__(self):
        super(FileNullException, self).__init__(self, "your file is null!")


class FileTool:
    @staticmethod
    def load_json_file(path):
        try:
            f = open(path, 'r+')
            conf = json.load(f, encoding='utf-8')
            f.close()
            return conf
        except Exception as e:
            raise e;

    @staticmethod
    def load_json_file_dict(path):
        conf = FileTool.load_json_file(path)
        if isinstance(conf, types.NoneType):
            print "%s is error,please check it\n"%(path)
            raise FileNullException

        if not isinstance(conf, dict):
            print "file content is not a dict\n"
            raise JsonNotDictException

        return conf