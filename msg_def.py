#!/usr/bin/python
# -*- coding:UTF-8 -*-

import struct
import socket


SEND_MSG_MAX_LEN = 2048 # 消息包最大长度
RECV_BUF_MAX_LEN = 2048 # 一次recv最大长度

class MSG_TYPE:
    HB              = 0 # 心跳包
    FIO             = 1 # FIO
    FIO_ANS         = 2 # FIO应答
    FIO_REPORT      = 3 # 压测报告
    FIO_REPORT_ANS  = 4 # 压测报告应答
    FIOSTOP         = 5 # FIO STOP
    FIOSTOP_ANS     = 6 # FIOSTOP应答
    ENGINEXIT       = 7 # 引擎退出


HEADERLEN = 42  # 消息头固定长度
# struct Header
# {
#     unsigned short no
#     unsigned short type
#     unsigned short has_next
#     char[32] expand
#     int      msg_len
# }


# 通信包结构
# {
#     "type":HB,
#     "has_next":0, 是否有后续包 0 无 1 有
#     "expand":[], 扩充参数
#     "data":""   字符串
# }


# # 消息打包
# def MakePkg(no, type, data, expand = [], has_next = 0):
#     msg = {}
#     msg["no"] = no
#     msg["type"] = type
#     msg["has_next"] = has_next
#     msg["expand"] = expand
#
#     # ss = ""
#     # for i in range(0, 300):
#     #     ss += "china"
#
#     msg["data"] = data
#
#     return str(msg)
#     # return json.dumps(msg)

# # 消息解包
# def ParsePkg(msg):
#     # print msg
#     try:
#         # return json.loads(msg)
#         return eval(msg)
#     except ValueError as e:
#         print e
#         return {}


# 打包消息头
def MakePkgHeader(no, type, body_len, has_next = 0, expand = "", ):
    """

    :param no:        消息序号
    :param type:      消息类型
    :param body_len:  消息体长度
    :param has_next:  是否还有后续包
    :param expand:    扩展参数
    :return:
    """
    msg_header = struct.pack("!HHHi32s", no, type, body_len, has_next, expand)
    return msg_header


def ParsePkgHeader(msg):
    msg_header = struct.unpack("!HHHi32s", msg)
    return msg_header


# 获取完整的数据
def recv_all(socket_fd, size):
    try:
        msg = socket_fd.recv(size)
    except socket.error as e:
        print "[error]: %s" % e
        return ""

    if len(msg) == 0:
        print "[error]: connection is closed!"
        return ""

    elif len(msg) == size:
        return msg

    elif len(msg) < size:    # 后台将包拆分了，所以此处要拼包
        e = size - len(msg)
        while(e > 0):
            try:
                data = socket_fd.recv(e)
            except socket.error as e:
                print "[error]: %s" % e
                return ""

            if len(data) == 0:
                print "[error]: connection is closed!"
                return ""
            msg += data
            e = e - len(data)

    return msg


# if __name__ == "__main__":
    # import struct
    # import binascii
    # import ctypes

    # ss =struct.pack("!HH32si", MSG_TYPE.FIO, 0, "dfakasdl", 256)
    # print len(ss)
    # print repr(ss) 
    # print struct.unpack("!HH32si", ss)[2]
    # print struct.unpack("!HH32si", ss)
