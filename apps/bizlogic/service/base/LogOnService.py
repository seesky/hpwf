# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2018/12/11 17:04'

def LogOnByOpenId(openId, returnStatusCode, returnStatusMessage):
    pass

def LogOnByUserName(userName, returnStatusCode, returnStatusMessage):
    pass

def UserLogOn(userName, password, openId, craeteOpenId, returnStatusCode, returnStatusMessage):
    pass

def GetEntity(id):
    pass

def Update(entity):
    pass

def GetUserDT():
    pass

def GetStaffUserDT():
    pass

def AccountActivation(openId, statusCode, statusMessage):
    pass

def OnLine(onLineState=1):
    pass

def OnExit():
    pass

def ServerCheckOnLine():
    pass

def SetPassword(userIds, password, returnStatusCode, returnStatusMessage):
    pass

def ChangePassword(oldPassword, newPassword, statusCode, statusMessage):
    pass

def UserIsLogOn():
    pass

def LockUser(userName):
    pass

def UnLockUser(userName):
    pass

def UserDimission(userName, dimissionCause, dimissionDate, dimissionWhither=None):
    pass