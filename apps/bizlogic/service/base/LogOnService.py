# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2018/12/11 17:04'

class LogOnService(object):

    def LogOnByOpenId(self, openId, returnStatusCode, returnStatusMessage):
        pass

    def LogOnByUserName(self, userName, returnStatusCode, returnStatusMessage):
        pass

    def UserLogOn(self, userName, password, openId, craeteOpenId, returnStatusCode, returnStatusMessage):
        pass

    def GetEntity(self, id):
        pass

    def Update(self, entity):
        pass

    def GetUserDT(self):
        pass

    def GetStaffUserDT(self):
        pass

    def AccountActivation(self, openId, statusCode, statusMessage):
        pass

    def OnLine(self, onLineState=1):
        pass

    def OnExit(self):
        pass

    def ServerCheckOnLine(self):
        pass

    def SetPassword(self, userIds, password, returnStatusCode, returnStatusMessage):
        pass

    def ChangePassword(self, oldPassword, newPassword, statusCode, statusMessage):
        pass

    def UserIsLogOn(self):
        pass

    def LockUser(self, userName):
        pass

    def UnLockUser(self, userName):
        pass

    def UserDimission(self, userName, dimissionCause, dimissionDate, dimissionWhither=None):
        pass