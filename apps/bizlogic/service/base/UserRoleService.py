# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2018/12/11 16:17'

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
        roleId = Pirole.objects.get(Q(deletemark=0) & Q(code=roleCode))
        if not roleId:
            return False
        roleIds = UserRoleService.GetAllRoleIds(self, roleId)
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
            sqlQuery = 'select roleid from piuser where (id=\'' + userId + '\') AND '
            sqlQuery = sqlQuery + '(deletemark=0) AND '
            sqlQuery = sqlQuery + ' (enabled=1) union select roleid from piuserrole where (userid=\'' + userId + '\') AND '
            sqlQuery = sqlQuery + '(roleid in (select id from pirole where (deletemark = 0 ))) AND (deletemark=0)'

            q1 = Piuser.objects.filter(Q(id=userId) & Q(deletemark=0) & Q(enabled=1)).values('roleid')
            q2 = Piuserrole.objects.filter(Q(userid=userId) & Q(roleid__in=Pirole.objects.filter(deletemark=0).values('id')) & Q(deletemark=0)).values('roleid')
            returnValue = q1.union(q2)

