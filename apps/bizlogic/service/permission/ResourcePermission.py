# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2018/12/12 8:27'

def GetResourcePermissionItemIds(resourceCategory, resourceId):
    pass

def GrantResourcePermission(resourceCategory, resourceId, grantPermissionItemIds):
    pass

def RevokeResourcePermission(resourceCategory, resourceId, revokePermissionItemIds):
    pass

def GetPermissionScopeTargetIds(resourceCategory, resourceId, targetCategory, permissionItemCode):
    pass

def GetPermissionScopeResourceIds(resourceCategory, targetId, targetResourceCategory, permissionItemCode):
    pass

def GrantPermissionScopeTargets(resourceCategory, resourceId, targetCategory, grantTargetIds, permissionItemId):
    pass

def GrantPermissionScopeTarget(resourceCategory, resourceIds, targetCategory, grantTargetId, permissionItemId):
    pass

def RevokePermissionScopeTargets(resourceCategory, resourceId, targetCategory, revokeTargetIds, permissionItemId):
    pass

def RevokePermissionScopeTarget(resourceCategory, resourceIds, targetCategory, revokeTargetId, permissionItemId):
    pass

def ClearPermissionScopeTarget(resourceCategory, resourceId, targetCategory, permissionItemId):
    pass

def GetResourceScopeIds(userId, targetCategory, permissionItemCode):
    pass

def GetTreeResourceScopeIds(userId, targetCategory, permissionItemCode, childrens):
    pass