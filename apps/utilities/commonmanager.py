# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2018/12/12 16:25'

from .message.StatusCode import StatusCode

class CommonManager():

    def GetStateMessage(self, statusCode):
        if statusCode.strip() == '':
            return ''
        status = StatusCode(statusCode)

    def GetStateMessage(self, statusCode):
        returnValue = StatusCode.statusCodeDic(statusCode)