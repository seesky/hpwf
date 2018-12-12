# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2018/12/11 16:02'

import apps.bizlogic.models


class ExceptionService(object):
    def Add(self, entity, statusCode, statusMessage):
        pass

    def GetDT(self):
        pass

    def GetDTByPage(self, recordCount, pageIndex=1, pageSize=20, whereConditional="", order=""):
        pass

    def GetEntity(self, id):
        pass

    def GetDTByValues(self, names, values):
        pass

    def Delete(self, id):
        pass

    def BatchDelete(self, ids):
        pass

    def Truncate(self):
        pass