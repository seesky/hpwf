# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2018/12/12 8:52'

from apps.bizlogic.models import Piuser
from apps.bizlogic.models import Piuserrole
from apps.bizlogic.models import Pipermission
from apps.bizlogic.models import Pipermissionscope

from django.db.models import Q

class UserPermission(object):

    def GetUserPermissionItemIds(self, userId):
        pass

    def GetUserIdsByPermissionItemId(self, permissionItemId):
        pass

    def GrantUserPermissions(self, userIds, grantPermissionItemIds):
        pass

    def GrantUserPermissionById(self, userId, grantPermissionItemId):
        pass

    def RevokeUserPermissions(self, userIds, revokePermissionItemIds):
        pass

    def RevokeUserPermissionById(self, userId, revokePermissionItemId):
        pass

    def GetScopeOrganizeIdsByUserId(self, userId, permissionItemCode):
        pass

    def GrantUserOrganizeScope(self, userId, permissionScopeItemCode, grantOrganizeIds):
        pass

    def RevokeUserOrganizeScope(self, userId, permissionScopeItemCode, revokeOrganizeIds):
        pass

    def GetScopeUserIdsByUserId(self, userId, permissionItemCode):
        pass

    def GrantUserUserScope(self, userId, permissionScopeItemCode, grantUserIds):
        pass

    def RevokeUserUserScope(self, userId, permissionScopeItemCode, revokeUserIds):
        pass

    def GetScopeRoleIdsByUserId(self, userId, permissionItemCode):
        pass

    def GrantUserRoleScope(self, userId, permissionScopeItemCode, grantRoleIds):
        pass

    def RevokeUserRoleScope(self, userId, permissionScopeItemCode, revokeRoleIds):
        pass

    def GetScopePermissionItemIdsByUserId(self, userId, permissionItemCode):
        pass

    def GrantUserPermissionItemScope(self, userId, permissionItemCode, grantPermissionItemIds):
        pass

    def RevokeUserPermissionItemScope(self, userId, permissionItemCode, revokePermissionItemIds):
        pass

    def ClearUserPermissionByUserId(self, userId):
        """
        清除指定用户的所有权限
        1.清除用户的角色归属
        2.清除用户的模块权限
        3.清除用户的操作权限
        Args:
            id (string): 用户主键
        Returns:
            returnValue (True or False): 清除结果
        """

        try:
            #清除用户的角色归属
            user = Piuser.objects.get(id=userId)
            user.roleid = None
            user.save()
            Piuserrole.objects.filter(userid=userId).delete()
            #清除用户的模块权限
            Pipermission.objects.filter(Q(resourcecategory=Piuser._meta.db_table) & Q(resourceid=userId)).delete()
            #清除用户的操作权限
            Pipermissionscope.objects.filter(Q(resourcecategory=Piuser._meta.db_table) & Q(resourceid=userId)).delete()
            return True
        except Exception as e:
            print(e)
            return False


    def ClearUserPermissionScope(self, userId, permissionItemCode):
        pass

    def GetModuleIdsByUserId(self, userId):
        pass

    def GetModuleDT(self):
        pass

    def GetModuleDTByUserId(self, userId):
        pass

    def GetScopeModuleIdsByUserId(self, userId, permissionItemCode):
        pass

    def GrantUserModuleScope(self, userId, permissionScopeItemCode, grantModuleIds):
        pass

    def GrantUserModuleScope(self, userId, permissionScopeItemCode, grantModuleId):
        pass

    def RevokeUserModuleScope(self, userId, permissionScopeItemCode, revokeModuleId):
        pass

    def RevokeUserModuleScope(self, userId, permissionScopeItemCode, revokeModuleIds):
        pass