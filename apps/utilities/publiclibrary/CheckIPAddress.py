# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2018/12/27 10:50'

from apps.bizlogic.models import Ciparameter
from django.db.models import Q

class CheckIPAddress(object):

    def CheckIPAddress(self, ipAddress, userId):
        """
        检查用户IP地址
        Args:
            ipAddress (string): IP地址
            userId (string): 用户主键
        Returns:
            returnValue(True or False): 是否符合限制
        """
        returnValue = False

        dt = Ciparameter.objects.filter(Q(parameterid=userId) & Q(categorykey='IPAddress') & Q(enabled=1))
        if dt.count() > 0:
            parameterCode = ''
            parameterCotent = ''
            for p in dt:
                parameterCode = p.parametercode
                parameterCotent = p.parametercontent
                if parameterCode == 'Single':
                    returnValue = self.CheckSingleIPAddress(ipAddress, parameterCotent)
                elif parameterCode == 'Range':
                    returnValue = self.CheckIPAddressWithRange(ipAddress, parameterCotent)
                elif parameterCode == 'Mask':
                    returnValue = CheckIPAddressWithMask(ipAddress, parameterCotent)
                else:
                    pass
                if returnValue:
                    break
        return returnValue


    def CheckSingleIPAddress(self, ipAddress, sourceIp):
        """
        检查是否匹配单个IP
        Args:
            ipAddress (string): IP地址
            sourceIp (string): 源IP
        Returns:
            returnValue(True or False): 是否符合限制
        """
        if ipAddress == sourceIp:
            return True
        else:
            return False


    def CheckIPAddressWithRange(self, ipAddress, ipRange):
        #先判断符合192.168.0.1-192.168.0.10 的正则表达式
        startIp = ipRange.split('-')[0]
        endIp = ipRange.split('-')[1]
        return self.CompareIp(self, ipAddress, startIp) == 2 and self.CompareIp(self, ipAddress, endIp) == 0 or self.CompareIp(self, ipAddress, startIp) == 1 or self.CompareIp(self, ipAddress, endIp) == 1

    def CompareIp(self, ip1, ip2):
        """
        比较两个IP地址，比较前可以先判断是否是IP地址
        Args:
            ip1 (string): IP1
            ip2 (string): IP2
        Returns:
            returnValue(0 1 2 -1): 1：相等;  0：ip1小于ip2 ; 2：ip1大于ip2；-1 不符合ip正则表达式
        """
        arr1 = ip1.split('.')
        arr2 = ip2.split('.')
        for i in range(0, arr1.len()):
            a1 = int(arr1[i])
            a2 = int(arr2[i])
            if a1 > a2:
                return 2
            elif a1 < a2:
                return 0
        return 1
