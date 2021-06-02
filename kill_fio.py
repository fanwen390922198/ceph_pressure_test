#!/usr/bin/python
# -*- coding:UTF-8 -*-

# Copyright (C) 2017 - All Rights Reserved
# 模块名称: kill_fio.py
# 创建日期: 2017/12/27 15:18
# 代码编写: fanwen
# 功能说明:

from base_lib.bat_operate_tool import CBatOperate


vm_list = ["vmtest1","vmtest2","vmtest3","vmtest4","vmtest5","vmtest6","vmtest7","vmtest8","vmtest9","vmtest10","vmtest11"];


if __name__ == "__main__":
    bo = CBatOperate();
    for vm in vm_list:
        bo.run_cmd_on_one_remote(vm, "ps -ef|grep fio|grep -v grep|cut -c 9-15|xargs kill -s 9");
