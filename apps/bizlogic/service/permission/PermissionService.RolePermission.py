# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2018/12/12 8:36'

def GetRolePermissionItemIds(roleId):
    pass

def GetRoleIdsByPermissionItemId(permissionItemId):
    pass

def GrantRolePermissions(roleIds, grantPermissionItemIds):
    pass

def GrantRolePermission(roleName, permissionItemCode):
    pass

def GrantRolePermissionById(roleId, grantPermissionItemId):
    pass

def RevokeRolePermissions(roleIds, revokePermissionItemIds):
    pass

def RevokeRolePermission(roleName, permissionItemCode):
    pass

def RevokeRolePermissionById(roleId, revokePermissionItemId):
    pass

def GetScopeUserIdsByRoleId(roleId, permissionItemCode):
    pass

def GetScopeRoleIdsByRoleId(roleId, permissionItemCode):
    pass

def GetScopeOrganizeIdsByRoleId(roleId, permissionItemCode):
    pass

def GrantRoleUserScope(roleId, permissionItemCode, grantUserIds):
    pass

def RevokeRoleUserScope(roleId, permissionItemId, revokeUserIds):
    pass

def GrantRoleRoleScope(roleId, permissionItemCode, grantRoleIds):
    pass

def RevokeRoleRoleScope(roleId, permissionItemId, revokeRoleIds):
    pass

def GrantRoleOrganizeScope(roleId, permissionItemCode, grantOrganizeIds):
    pass

def RevokeRoleOrganizeScope(roleId, permissionItemId, revokeOrganizeIds):
    pass

def GetScopePermissionItemIdsByRoleId(roleId, permissionItemCode):
    pass

def GrantRolePermissionItemScope(roleId, permissionItemCode, grantPermissionItemIds):
    pass

def RevokeRolePermissionItemScope(roleId, permissionItemCode, revokePermissionItemIds):
    pass

def ClearRolePermissionScope(roleId, permissionItemCode):
    pass

def ClearRolePermissionByRoleId(roleId):
    pass

def GetScopeModuleIdsByRoleId(roleId, permissionItemCode):
    pass

def GrantRoleModuleScope(roleId, permissionItemCode, grantModuleIds):
    pass

def GrantRoleModuleScope(roleId, permissionItemCode, grantModuleId):
    pass

def RevokeRoleModuleScope(roleId, permissionItemCode, revokeModuleIds):
    pass

def RevokeRoleModuleScope(roleId, permissionItemCode, revokeModuleId):
    pass