# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2018/12/11 17:25'

class ParameterService(object):

    def GetServiceConfig(self, key):
        pass

    def GetParameter(self, categoryKey, parameterId, parameterCode):
        pass

    def GetEntity(self, id):
        pass

    def SetParameter(self, categoryKey, parameterId, parameterCode, parameterContent, allowEdit=0, allowDelete=0):
        pass

    def GetDTByParameter(self, categoryKey, parameterId):
        pass

    def GetListByParameter(self, categoryKey, parameterId):
        pass

    def GetDTByParameterCode(self, categoryKey, parameterId, parameterCode):
        pass

    def GetListByParameterCode(self, categoryKey, parameterId, parameterCode):
        pass

    def GetDTByPage(self, recordCount, pageIndex=1, pageSize=20, whereConditional="", order=""):
        pass

    def SetDeleted(self, id):
        pass

    def DeleteByParameter(self, categoryKey, parameterId):
        pass

    def DeleteByParameterCode(self, categoryKey, parameterId, parameterCode):
        pass

    def Delete(self, id):
        pass

    def BatchDelete(self, ids):
        pass