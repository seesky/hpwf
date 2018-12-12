# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2018/12/11 15:41'

def WriteLog(processId, processName, methodId, methodName):
    pass

def WriteExit(logId):
    pass

def GetLogGeneral():
    pass

def GetDTByDate(beginDate, endDate, userId, moduleId):
    pass

def GetDTByModule(processId, beginDate, endDate):
    pass

def GetDTByUser(userId, beginDate, endDate):
    pass

def GetDTByPage(recordCount, pageIndex=1, pageSize=20, whereConditional="", order=""):
    pass

def Delete(id):
    pass

def BatchDelete(ids):
    pass

def Truncate():
    pass

def GetDTApplicationByDate(beginDate, endDate):
    pass

def BatchDeleteApplication(ids):
    pass

def TruncateApplication():
    pass