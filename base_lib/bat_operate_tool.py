#!/usr/bin/python
# -*- coding:UTF-8 -*-
#     Copyright (C) 2017 - All Rights Reserved
#     模块名称: bat_operate_tool.py
#     创建日期: 2017/11/29 15:49
#     代码编写: fanwen
#     功能说明:
#     基于scp命令和dsh写一个批量传递文件和执行命令的类，dsh 需要配置无密码访问，请使用前做相关的配置，
# 在Python中可以使用paramiko或者pexpect来处理类似ssh操作

# 如果使用源安装失败的话, 请使用手动安装相关工具!!!
#
# dsh工具安装方法:
# wget http://www.netfort.gr.jp/~dancer/software/downloads/libdshconfig-0.20.9.tar.gz
# tar zxvf libdshconfig-0.20.9.tar.gz
# cd libdshconfig-0.20.9
# ./configure
# make && make install
# # 注意生成的库文件在./libs中
#
# wget http://www.netfort.gr.jp/~dancer/software/downloads/dsh-0.25.9.tar.gz
# tar zxvf dsh-0.25.9.tar.gz
# cd dsh-0.25.9
# ./configure --prefix=/usr/
# make && make install
#
# ln -s /usr/local/lib/libdshconfig.so.1 /lib64/
import os
from szt_sys import run_cmd
from szt_sys import get_platform
from szt_log import Log


class CBatOperate:
    def __init__(self):
        self.platform = get_platform()
        self.h_log = Log("batcmd", "bat_operate", False)

    def __install_dsh(self):
        """
            在“控制”节点上安装dsh工具
        """
        source_type = "apt-get" if self.platform == "Ubuntu" else "yum"
        if run_cmd("%s install dsh" % source_type, log_handle = self.h_log)[0] != 0:
            print "dsh install failed!"

    def copy_file_to_remote(self, remote, source_file, remote_file_path):
        """
        将文件从"控制"节点复制到远程机器上
        :param remote: 远程机器名或者IP
        :param source_file: 待拷贝的文件
        :param remote_file_path: 远程机器上防止拷贝文件的目录
        :return: 返回运行结果
        """
        cmd = "scp %s root@%s:%s" % (source_file, remote, remote_file_path)
        run_cmd(cmd, log_handle = self.h_log)

    def bat_copy_file_to_remote(self, remote_list, source_file, remote_file_path):
        """
        批量执行远程复制命令
        :param remote_list: 远程机器名或者IP列表
        :param source_file: 待拷贝的文件
        :param remote_file_path: 远程机器上防止拷贝文件的目录
        :return: 返回运行结果
        """
        for remote in remote_list:
            self.copy_file_to_remote(remote, source_file, remote_file_path)

    def bat_copy_file_from_remote2(self, remote, remote_file_path, file_path):
        """
        :param remote:
        :param remote_file_path:
        :param file_path:
        :return:
        """
        cmd = "scp root@%s:%s %s" % (remote, remote_file_path, file_path)
        run_cmd(cmd, log_handle=self.h_log)

    def bat_copy_file_from_remote(self, remote_list, remote_file_path, file_path):
        """
        :param remote_list:
        :param remote_file_path:
        :param source_file:
        :return:
        """
        dir_file = os.path.split(file_path)
        end_file = []
        for remote in remote_list:
            file_name = remote + "-" + dir_file[1]
            end_file.append(file_name)

            if len(dir_file[0]) > 0:
                file_name = dir_file[0] + '/' + file_name
            cmd = "scp root@%s:%s %s" % (remote, remote_file_path, file_name)
            run_cmd(cmd, log_handle=self.h_log)
        return end_file

    def run_cmd_on_one_remote(self, remote, cmd):
        """
        在单个机器上执行命令
        :param remote: 远程机器名或者IP，注意一定要出现在hosts中
        :param cmd: 执行的SHELL命令
        :return: 返回运行结果，或者错误信息
        """
        dsh_cmd = "dsh -m %s -r ssh -- \'%s\'" % (remote, cmd)
        return run_cmd(dsh_cmd, log_handle = self.h_log)

    def run_cmd_on_group_remote(self, group_remote_file, cmd):
        """
        对分组的远程机器执行命令
        :param group_remote_file: 配置有远程机器信息的文件路径
        :param cmd: 待执行的命令
        :return: 返回运行结果，或者错误信息
        """
        dsh_cmd = "dsh -M -f %s -r ssh -- \'%s\'" % (group_remote_file, cmd)
        return run_cmd(dsh_cmd, log_handle = self.h_log)

    def run_cmd_on_group_remote2(self, group_remote_list, cmd):
        """
        对分组的远程机器执行命令，这个函数是为了防止有些人担心，dsh执行过程中出现异常，故采取遍历执行
        :param group_remote_list: 配置有远程机器信息的列表
        :param cmd: 待执行的命令
        :return: 返回运行结果，或者错误信息
        """
        for remote in group_remote_list:
            self.run_cmd_on_one_remote(remote, cmd)

# if __name__  == "__main__":
#     bp = CBatOperate()
#     vm_list = ["vmtest1", "vmtest2", "vmtest3", "vmtest4", "vmtest5", "vmtest6", "vmtest7", "vmtest8"]
#     bp.run_cmd_on_group_remote2(vm_list, "fdisk -l")

    # print "---------test copy---------"
    # bp.copy_file_to_remote("rgw1", "/root/getcode.sh", "/root/")
    #
    # print "---------test bat copy--------"
    # bp.bat_copy_file_to_remote(["rgw1","rgw12"], "/root/mycrushmap.txt", "/root/")
    #
    # print "---------test run cmd on one remote--------"
    # bp.run_cmd_on_one_remote("rgw1", "/bin/ls -l /root/mycrushmap.txt")
    #
    # print "---------test run cmd on group remote--------"
    # bp.run_cmd_on_group_remote("/root/dsh_host", "/bin/ls -l /root/mycrushmap.txt")
    #
    # print "---------test run cmd on remote_list--------"
    # bp.run_cmd_on_group_remote2(["rgw1","rgw12"], "/bin/ls -l /root/mycrushmap.txt")
    #
    # print "---------test run cmd on remote_list--------"
    # bp.run_cmd_on_group_remote("/root/dsh_host", "ps -elf|grep ceph")
    #
    # print "---------test run cmd on remote_list--------"
    # bp.run_cmd_on_group_remote2(["rgw1","rgw12"], "ceph -v")
