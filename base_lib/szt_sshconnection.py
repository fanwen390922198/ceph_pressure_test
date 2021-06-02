#!/usr/bin/python
# -*- coding:UTF-8 -*-
# 	Copyright (C) 2017 - All Rights Reserved
# 	模块名称: szt_sshconnection.py
# 	创建日期: 2017/9/7 13:27
# 	代码编写: fanwen
# 	功能说明:

import paramiko
import szt_log

class SSHConnection(object):
    def __init__(self, host, port, username, password):
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._transport = None
        self._sftp = None
        self._client = None
        self.log = szt_log.Log(self._host);
        self._connect()  # 建立连接

    def _connect(self):
        try:
            paramiko.util.log_to_file('ssh.log')  # 写日志文件
            transport = paramiko.Transport((self._host, self._port))
            transport.connect(username=self._username, password=self._password)
            self._transport = transport
            # 此处会相关相关的日志
            self.log.info("connected to host: %s"%self._host);

        except Exception, e:
            print e;

    # 下载
    def download(self, remotepath, localpath):
        if self._sftp is None:
            self._sftp = paramiko.SFTPClient.from_transport(self._transport)
        try:
            self._sftp.get(remotepath, localpath)
        except:
            self.log.error("down [%s] failed!"%remotepath);
            return False;

        self.log.info("down [%s] success!" % remotepath);
        return True;

    # 上传
    def put(self, localpath, remotepath):
        if self._sftp is None:
            self._sftp = paramiko.SFTPClient.from_transport(self._transport)
        try:
            self._sftp.put(localpath, remotepath)
        except Exception, e:
            self.log.error("put [%s] failed!" % localpath);
            self.log.error("reason: %s \n" % e.message);
            return False;

        self.log.info("put [%s] success!" % localpath);
        return True;

    # 执行命令
    def exec_command(self, command):
        self.log.info("Running command: %s"%command);
        if self._client is None:
            self._client = paramiko.SSHClient()
            self._client._transport = self._transport
        try:
            stdin, stdout, stderr = self._client.exec_command(command)
            data = stdout.read()
            if len(data) > 0:
                dataline = data.split('\n');
                for line in dataline:
                    self.log.info(line.strip()); # 打印正确结果

            err = stderr.read()
            if len(err) > 0:
                dataline = err.split('\n');
                for line in dataline:
                    self.log.error(line.strip()); # 打印错误信息

            return [data.strip(), err.strip()];

        except Exception, e:
            #self.log.exception(err.strip());  #
            print e;

    def close(self):
        if self._transport:
            self._transport.close()
        if self._client:
            self._client.close()


# if __name__ == "__main__":
#     conn = SSHConnection("127.0.0.1", 22, "root", "");
    #conn.exec_command("cd fanwen; pwd; ls -l");
    #conn.exec_command("pwd");
    #conn.put("szt_sys.py", "/root/fanwen/szt_sys.py");

    # conn.download("/root/fanwen/paramiko.tar.gz", "paramiko.tar.gz");
    # conn.download("/root/fanwen/python-ecdsa.tar.gz", "python-ecdsa.tar.gz");
    # conn.download("/root/fanwen/python-bcrypt.tar.gz", "python-bcrypt.tar.gz");
    # conn.download("/root/fanwen/pynacl.tar.gz", "pynacl.tar.gz");
    # conn.put("autoconf-2.69.tar.gz", "/root/fanwen/autoconf-2.69.tar.gz");
    # conn.download("/root/fanwen/libffi-1.tar.gz", "libffi-1.tar.gz");
    # conn.put("openssl-1.1.0g.tar.gz", "/root/fanwen/openssl-1.1.0g.tar.gz");


    # conn.exec_command("rpm -qa | grep xfsprogs");
    # conn.exec_command("rpm - qa | grep fanwen");

    # conn.close();

