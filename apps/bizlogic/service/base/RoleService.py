# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2018/12/11 16:29'

class RoleService(object):

    def Add(self, entity, statusCode, statsMessage):
        pass

    def Update(self, entity, statsCode, statusMessage):
        pass

    def GetDT(self):
        pass

    def GetList(self):
        pass

    def GetDtByPage(self, recordCount, pageIndex=1, pageSize=20, whereConditional="", order=""):
        pass

    def GetEntity(self, id):
        pass

    def GetDTByIds(self, ids):
        pass

    def GetDTByValues(self, names, values):
        pass

    def GetDTByOrganize(self, organizeId, showUser=True):
        pass

    def GetApplicationRole(self):
        pass

    def BatchSave(self, entites):
        pass

    def Delete(self, id):
        pass

    def BatchDelete(self, ids):
        pass

    def SetDeleted(self, ids):
        pass

    def EliminateRoleUser(self, roleId):
        pass

    def GetRoleUserIds(self, roleId):
        pass

    def AddUserToRole(self, roleId, addUserIds):
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