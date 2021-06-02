#!/usr/bin/python
# -*- coding:UTF-8 -*-
'''
	Copyright (C) 2017 - All Rights Reserved
	模块名称: szt_log.py
	创建日期: 2017/9/27 13:18
	代码编写: fanwen
	功能说明:

'''

import logging, time
import logging.handlers
from logging import Logger
import os
import sys


def currentframe():
    """Return the frame object for the caller's stack frame."""
    try:
        raise Exception
    except:
        return sys.exc_info()[2].tb_frame.f_back

# _srcfile = os.path.normcase(currentframe.__code__.co_filename)


class MyLogger(Logger):
    def __init__(self, name):
        Logger.__init__(self, name);

    def findCaller(self):
        f = currentframe()
        cur_f = __file__;
        if f is not None:
            f = f.f_back;

        while f is not None:
            if cmp(os.path.splitext(cur_f)[0], os.path.splitext(f.f_code.co_filename)[0]) == 0:
                f = f.f_back;
                break;
            f = f.f_back;

        rv = "(unknown file)", 0, "(unknown function)"

        while hasattr(f, "f_code"):
            co = f.f_code
            # filename = os.path.normcase(co.co_filename)
            # if filename == _srcfile:
            if cmp(os.path.splitext(os.path.split(cur_f)[1])[0],
                      os.path.splitext(os.path.split(f.f_code.co_filename)[1])[0]) == 0:
                if f.f_back <> None:
                    f = f.f_back
                    continue
            rv = (co.co_filename, f.f_lineno, co.co_name)
            break

        return rv


class Log(object):
    def __init__(self, log_flag, log_file, console=True):
        """
        :param log_flag: 日志标签
        :param log_file: 日志文件名(不含后缀)
        :param console:  是否需要往控制台输出
        """
        path = os.getcwd();
        today = time.strftime('%Y%m%d', time.localtime(time.time()));
        filename = path + '/%s-%s.log' % (log_file, today);

        Logger.manager.setLoggerClass(MyLogger);

        self.logger = logging.getLogger(log_flag);

        if len(self.logger.handlers) == 0:  # 此处判断一下是否已经建立了handle

            self.logger.setLevel(logging.DEBUG);
            fm = logging.Formatter('[%(asctime)s][%(name)s][%(levelname)s][%(module)s(line:%(lineno)d)]: %(message)s');

            # 日志保留10天,一天保存一个文件
            file_handler = logging.handlers.TimedRotatingFileHandler(filename, 'D', 1, 10);

            # 定义日志文件中格式
            file_handler.setFormatter(fm);
            self.logger.addHandler(file_handler);

            if console:
                # 控制台输出handler
                console_handler = logging.StreamHandler();
                console_handler.setFormatter(fm);
                self.logger.addHandler(console_handler);

        Logger.manager.setLoggerClass(Logger);

    def __del__(self):
        self.logger.handlers = [];

    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs);

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs);

    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs);

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs);

    def exception(self, msg, *args, **kwargs):
        self.logger.exception(msg, *args, **kwargs);


class customError(Exception):
    # 自定义异常类,用在主动输出异常时使用,用 raise关键字配合使用,例:
    #       if True:
    #             pass
    #       else:
    #             raise customError(msg)
    def __init__(self, msg=None):
        self.msg = msg

    def __str__(self):
        if self.msg:
            return self.msg
        else:
            return u"某个不符合条件的语法出问题了"


if __name__ == "__main__":

    # print currentframe();
    # print _srcfile;

    log = Log("TEST", "TEST");
    log.debug("this is test1 %s" % time.gmtime());
    # log.exception("exception1");

    # log2.debug("this is test2 %s"%time.gmtime());
    # log2.exception("exception2");
    #
    # log.debug("this is test1 %s"%time.gmtime());
    # log2.exception("exception2");

    logging.basicConfig(format = '[%(asctime)s][%(levelname)s][%(module)s(line:%(lineno)d)]:%(message)s', level = logging.DEBUG);
    log2 = logging.getLogger("orignal");
    log2.debug("hello logging");
