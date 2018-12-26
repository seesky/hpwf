# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2018/12/11 15:41'

class LogService(object):

    def WriteLog(self, processId, processName, methodId, methodName):
        pass

    def WriteExit(self, logId):
        pass

    def GetLogGeneral(self):
        pass

    def GetDTByDate(self, beginDate, endDate, userId, moduleId):
        pass

    def GetDTByModule(self, processId, beginDate, endDate):
        pass

    def GetDTByUser(self, userId, beginDate, endDate):
        pass

    def GetDTByPage(self, recordCount, pageIndex=1, pageSize=20, whereConditional="", order=""):
        pass

    def Delete(self, id):
        pass

    def BatchDelete(self, ids):
        pass

    def Truncate(self):
        pass

    def GetDTApplicationByDate(self, beginDate, endDate):
        pass

    def BatchDeleteApplication(self, ids):
        pass

    def TruncateApplication(self):
        pass