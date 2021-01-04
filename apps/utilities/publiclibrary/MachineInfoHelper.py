# _*_ coding: utf-8 _*_
__author__ = 'baxuelong@163.com'
__date__ = '2018/12/26 14:23'

import socket
import uuid

class MachineInfoHelper(object):

    def GetIPAddress(self):
        """
        获取本机IP地址
        Args:
        Returns:
            returnValue(string): 本机IP地址
        """
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8',80))
            ip = s.getsockname()[0]
        finally:
            s.close()
        return ip

    def GetMacAddress(self):
        """
        获取本机MAC地址
        Args:
        Returns:
            returnValue(string): 本机MAC地址
        """
        mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
        return ":".join([mac[e:e + 2] for e in range(0, 11, 2)])

    def GetHostname(self):
        """
        获取本机主机名
        Args:
        Returns:
            returnValue(string): 本机主机名
        """
        return socket.gethostname()