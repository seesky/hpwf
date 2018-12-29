# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2018/12/12 8:36'

class RolePermission(object):

    def GetRolePermissionItemIds(self, roleId):
        pass

    def GetRoleIdsByPermissionItemId(self, permissionItemId):
        pass

    def GrantRolePermissions(self, roleIds, grantPermissionItemIds):
        pass

    def GrantRolePermission(self, roleName, permissionItemCode):
        pass

    def GrantRolePermissionById(self, roleId, grantPermissionItemId):
        pass

    def RevokeRolePermissions(self, roleIds, revokePermissionItemIds):
        pass

    def RevokeRolePermission(self, roleName, permissionItemCode):
        pass

    def RevokeRolePermissionById(self, roleId, revokePermissionItemId):
        pass

    def GetScopeUserIdsByRoleId(self, roleId, permissionItemCode):
        pass

    def GetScopeRoleIdsByRoleId(self, roleId, permissionItemCode):
        pass

    def GetScopeOrganizeIdsByRoleId(self, roleId, permissionItemCode):
        pass

    def GrantRoleUserScope(self, roleId, permissionItemCode, grantUserIds):
        pass

    def RevokeRoleUserScope(self, roleId, permissionItemId, revokeUserIds):
        pass

    def GrantRoleRoleScope(self, roleId, permissionItemCode, grantRoleIds):
        pass

    def RevokeRoleRoleScope(self, roleId, permissionItemId, revokeRoleIds):
        pass

    def GrantRoleOrganizeScope(self, roleId, permissionItemCode, grantOrganizeIds):
        pass

    def RevokeRoleOrganizeScope(self, roleId, permissionItemId, revokeOrganizeIds):
        pass

    def GetScopePermissionItemIdsByRoleId(self, roleId, permissionItemCode):
        pass

    def GrantRolePermissionItemScope(self, roleId, permissionItemCode, grantPermissionItemIds):
        pass

    def RevokeRolePermissionItemScope(self, roleId, permissionItemCode, revokePermissionItemIds):
        pass

    def ClearRolePermissionScope(self, roleId, permissionItemCode):
        pass

    def ClearRolePermissionByRoleId(self, roleId):
        pass

    def GetScopeModuleIdsByRoleId(self, roleId, permissionItemCode):
        pass

    def GrantRoleModuleScope(self, roleId, permissionItemCode, grantModuleIds):
        pass

    def GrantRoleModuleScope(self, roleId, permissionItemCode, grantModuleId):
        pass

    def RevokeRoleModuleScope(self, roleId, permissionItemCode, revokeModuleIds):
        pass

    def RevokeRoleModuleScope(self, roleId, permissionItemCode, revokeModuleId):
        pass