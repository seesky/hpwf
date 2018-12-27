# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2018/12/12 8:14'

from apps.bizlogic.models import Piuser
from apps.bizlogic.service.base.UserRoleService import UserRoleService
from apps.utilities.message.DefaultRole import DefaultRole
from apps.bizlogic.models import Pirole

class PermissionService(object):

    def IsInRole(self, userId, roleName):
        pass

    def IsAuthorized(self, permissionItemCode, permissionItemName=None):
        pass

    def IsAuthorizedByUserId(self, userId, permissionItemCode, permissionItemName=None):
        pass

    def IsAuthorizedByRoleId(self, roleId, permissionItemCode):
        pass

    def IsAdministrator(self, entity):
        """
        当前用户是否超级管理员
        Args:
            userInfo (UserInfo): 用户
        Returns:
            returnValue(True or False): 当前用户是否为超级管理员，true：是，false：否
        """
        returnValue = False
        userEntity = Piuser.objects.get(id=entity.Id)
        if userEntity.id == 'Administrator':
            return True
        if userEntity.code and userEntity.code == 'Administrator':
            return True
        if userEntity.username and userEntity.username == 'Administrator':
            return True

        #TODO:if (this.UserInfo == null) return false;

        #用户的默认角色是超级管理员
        roleEntity = None
        if userEntity.roleid:
            roleIds = UserRoleService.GetRoleIds(self, userEntity.id)
            for tmpid in roleIds:
                if tmpid == DefaultRole.Administrators:
                    return True
                roleEntity = Pirole.objects.get(id=tmpid)
                if roleEntity.code and roleEntity.code == DefaultRole.Administrators:
                    return True
        return False

    def IsAdministratorByUserId(self, userId):
        pass

    def GetPermissionDT(self):
        pass

    def GetPermissionDTByUserId(self, userId):
        pass

    def IsModuleAuthorized(self, moduleCode):
        pass

    def IsModuleAuthorizedByUserId(self, userId, moduleCode):
        pass

    def GetPermissionScopeByUserId(self, userId, permissionItemCode):
        pass