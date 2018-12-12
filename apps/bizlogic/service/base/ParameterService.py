# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2018/12/11 17:25'

def GetServiceConfig(key):
    pass

def GetParameter(categoryKey, parameterId, parameterCode):
    pass

def GetEntity(id):
    pass

def SetParameter(categoryKey, parameterId, parameterCode, parameterContent, allowEdit=0, allowDelete=0):
    pass

def GetDTByParameter(categoryKey, parameterId):
    pass

def GetListByParameter(categoryKey, parameterId):
    pass

def GetDTByParameterCode(categoryKey, parameterId, parameterCode):
    pass

def GetListByParameterCode(categoryKey, parameterId, parameterCode):
    pass

def GetDTByPage(recordCount, pageIndex=1, pageSize=20, whereConditional="", order=""):
    pass

def SetDeleted(id):
    pass

def DeleteByParameter(categoryKey, parameterId):
    pass

def DeleteByParameterCode(categoryKey, parameterId, parameterCode):
    pass

def Delete(id):
    pass

def BatchDelete(ids):
    pass