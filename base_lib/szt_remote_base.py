#!/usr/bin/python
# -*- coding:UTF-8 -*-
import szt_sshconnection


class CRemoteBase:
    def __init__(self, remote):
        self.hostname = remote.hostname;
        self.ip = remote.ip;
        self.port = remote.port;
        self._remote = remote;
        self.__create_conn();

    def __create_conn(self):
        self.sshconn = szt_sshconnection.SSHConnection( self.ip, self.port, self._remote.username, self._remote.password );

    def __del__(self):
        self.sshconn.close();


