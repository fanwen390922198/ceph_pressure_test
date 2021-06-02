#!/usr/bin/python
# -*- coding:UTF-8 -*-
# 	Copyright (C) 2017 - All Rights Reserved
# 	模块名称: szt_sys.py
# 	创建日期: 2017/9/6 15:44
# 	代码编写: fanwen
# 	功能说明:

import commands
import platform
import subprocess
import socket
import time
import datetime
import szt_log


# 增强版执行shell命令函数，采用子进程加管道,可实时打印输出
def run_cmd2(cmd):
    print "[info]: run cmd-->%s"%cmd
    try:
        process1 = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        data = ""
        while True:
           line = process1.stdout.readline()
           data += line
           if not line:
               break
           print "\t%s"%line.strip()

        error = process1.stderr.read()
        if len(error.strip()) > 0:
            print "[error]: %s"%error

        return [data, error]

    except Exception, e:
        print e
        return ["", e]


def run_cmd(cmd, need_print_correct_res = True, log_handle = None):
    """
    执行命令
    :param cmd: 待执行的命令行
    :param need_print_correct_res: 是否需要打印正确结果
    :param log_handle:  日志对象句柄(为szt_log.Log实例)
    :return: 返回执行结果
    """
    res = commands.getstatusoutput(cmd)
    if(res[0] != 0):
        if log_handle != None and isinstance(log_handle, szt_log.Log):
            log_handle.error('--------->> RUN [%s] Failed!' % cmd)
            log_handle.error("REASON: [%s] \n" % res[1])
        else:
            print "[error]: Run [%s] Failed!"%cmd
            print "[error]: Reason: [%s] \n" %res[1]

    else:
        if need_print_correct_res:
            if log_handle != None and isinstance(log_handle, szt_log.Log):
                log_handle.info('--------->> Run [%s] Success!' % cmd)
                log_handle.info("RESULT: [%s]" % res[1])
            else:
                print "[info]: --------->> Run [%s] Success!"%cmd
                print "[info]: RESULT: [%s]\n" %res[1]

    return res


def get_platform():
    if (platform.platform(True).find('Ubuntu') != -1):
        return "Ubuntu"
    elif (platform.platform(True).find('redhat') != -1):
        return "Redhat"
    elif (platform.platform(True).find('Windows') != -1):
        return "Windows"


def ping(ip):
    cmd = "ping -c 1 %s"%ip
    errstr = "100% packet loss"
    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)        
        out = p.stdout.read()
        if out.find(errstr) != -1:
            print "%s unreachable"%ip
            return False
        else:
            print "%s reachable" % ip
            return True
               
    except:
        return False


def telnet(ip, port):
    ret = False
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.settimeout(1)

    try:
        sk.connect((ip,port))
        ret = True
        print "%s:%d is OK\n" % (ip, port)
    except:
        print "%s:%d not connect\n"%(ip, port)

    sk.close()

    return ret


def get_time(type):
    if type is 0:
        return time.strftime('%Y%m%d', time.localtime(time.time()))
    elif type is 1:
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    elif type is 2: #包含毫秒
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')


class CRemote(object):
    def __init__(self, hostname, ip, port, usrname, password):
        self.hostname = hostname
        self.ip = ip
        self.port = port
        self.username = usrname
        self.password = password


def test_interface():
    #print ping("192.168.22.210")
    # print telnet("192.168.22.211", 80)
    run_cmd2("654234")
    run_cmd2("hostname")

# if __name__ == "__main__":
#     sys.exit(test_interface())


