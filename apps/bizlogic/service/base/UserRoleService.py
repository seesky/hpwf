# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2018/12/11 16:17'

import uuid

from django.db.models import Q

from apps.bizlogic.models import Piuserrole
from apps.bizlogic.models import Pirole
from apps.bizlogic.models import Piuser


class UserRoleService(object):

    def GetDTByRole(self, roleId):
        pass

    def GetListByRole(self, roleIds):
        pass

    def GetRoleDT(self):
        pass

    def UserInRole(self, userId, roleCode):
        returnValue = False
        if not roleCode:
            return False
        roleId = Pirole.objects.get(Q(deletemark=0) & Q(code=roleCode)).id
        if not roleId:
            return False
        roleIds = UserRoleService.GetAllRoleIds(self, userId)
        if roleId in roleIds:
            return True
        else:
            return False

    def SetDefaultRole(self, userId, roleId):
        pass

    def BatchSetDefaultRole(self, userIds, roleId):
        pass

    def GetUserRoleIds(self, userId):
        pass

    def GetAllUserRoleIds(self, userId):
        pass

    def AddUserToRole(self, userId, addRoleIds):
        pass

    def RemoveUserFromRole(self, userId, removeRoleIds):
        pass

    def ClearUserRole(self, userId):
        pass

    def GetAllRoleIds(self, userId):
        if not userId:
            return []
        else:
            # sqlQuery = 'select roleid from piuser where (id=\'' + userId + '\') AND '
            # sqlQuery = sqlQuery + '(deletemark=0) AND '
            # sqlQuery = sqlQuery + ' (enabled=1) union select roleid from piuserrole where (userid=\'' + userId + '\') AND '
            # sqlQuery = sqlQuery + '(roleid in (select id from pirole where (deletemark = 0 ))) AND (deletemark=0)'

            list1 = Piuser.objects.filter(Q(id=userId) & Q(deletemark=0) & Q(enabled=1)).values_list('roleid', flat=True)
            list2 = Piuserrole.objects.filter(Q(userid=userId) & Q(roleid__in=Pirole.objects.filter(deletemark=0).values('id')) & Q(deletemark=0)).values_list('roleid', flat=True)
            returnValue = list1.union(list2)
            return returnValue

    def EliminateRoleUser(self, roleId):
        """
        移除角色用户关联
        Args:
            id (string): 角色主键
        Returns:
            returnValue (int): 移除影响行数
        """
        returnValue = 0
        returnValue = Piuser.objects.filter(Q(roleid=roleId)).update(roleid=None)
        returnValue = returnValue + Piuserrole.objects.filter(roleid=roleId).delete()
        return returnValue

    def GetUserIds(self, roleId):
        """
        获取员工的角色主键数组
        Args:
            roleId (string): 角色主键
        Returns:
            returnValue (int): 用户主键列表
        """
        q1 = Piuser.objects.filter(Q(roleid=roleId) & Q(deletemark=0) & Q(enabled=1)).values_list('id', flat=True)
        q2 = Piuserrole.objects.filter(Q(roleid=roleId) & Q(userid__in=Piuser.objects.filter(deletemark=0).values_list('id', flat=True)) & Q(deletemark=0))
        returnValue = q1.union(q2)
        return returnValue

    def AddToRole(self, userId, roleId):
        """
        加入到角色
        Args:
            userId (string): 用户主键
            roleId (string): 角色主键
        Returns:
            returnValue (int): 影响行数
        """
        returnValue = 0
        try:
            Piuserrole.objects.get(Q(userid=userId) & Q(roleid=roleId) & Q(enabled=1) & Q(deletemark=0))
            return returnValue
        except Piuserrole.DoesNotExist as e:
            userrole = Piuserrole()
            userrole.userid = userId
            userrole.roleid = roleId
            userrole.enabled = 1
            userrole.deletemark = 0
            userrole.save()
            returnValue = 1
            return returnValue

    def AddToRolesR(self, userId, roleIds):
        returnValue = 0
        for roleid in roleIds:
            returnValue = returnValue + UserRoleService.AddToRole(self, userId, roleid)
        return returnValue

    def AddToRolesU(self, userIds, roleId):
        returnValue = 0
        for userid in userIds:
            returnValue = returnValue + UserRoleService.AddToRole(self, userid, roleId)
        return returnValue

    def RemoveFormRole(self, userId, roleId):
        return Piuserrole.objects.filter(Q(userid=userId) & Q(roleid=roleId)).delete()

    def RemoveFromRoleR(self, userId, roleIds):
        returnValue = 0
        for roleid in roleIds:
            returnValue = returnValue + UserRoleService.RemoveFormRole(self, userId, roleid)
        return returnValue

    def RemoveFromRoleU(self, userIds, roleId):
        returnValue = 0
        for userid in userIds:
            returnValue = returnValue + UserRoleService.RemoveFormRole(self, userid, roleId)
        return returnValue

    def ClearRoleUser(self, roleId):
        returnValue = 0
        Piuser.objects.filter(roleid=roleId).update(roleid=None)
        returnValue = returnValue + Piuserrole.objects.filter(roleid=roleId).delete()
        return returnValue

