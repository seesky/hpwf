# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2018/12/11 16:29'

def Add(entity, statusCode, statsMessage):
    pass

def Update(entity, statsCode, statusMessage):
    pass

def GetDT():
    pass

def GetList():
    pass

def GetDtByPage(recordCount, pageIndex=1, pageSize=20, whereConditional="", order=""):
    pass

def GetEntity(id):
    pass

def GetDTByIds(ids):
    pass

def GetDTByValues(names, values):
    pass

def GetDTByOrganize(organizeId, showUser=True):
    pass

def GetApplicationRole():
    pass

def BatchSave(entites):
    pass

def Delete(id):
    pass

def BatchDelete(ids):
    pass

def SetDeleted(ids):
    pass

def EliminateRoleUser(roleId):
    pass

def GetRoleUserIds(roleId):
    pass

def AddUserToRole(roleId, addUserIds):
    pass

def RemoveUserFromRole(roleId, userIds):
    pass

def ClearRoleUser(roleId):
    pass

def SetUsersToRole(roleId, userIds):
    pass

def ResetSortCode(organizeId):
    pass

def MoveTo(id, targetOrganizedId):
    pass