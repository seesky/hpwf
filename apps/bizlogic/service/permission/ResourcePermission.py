# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2018/12/12 8:27'

class ResourcePermission(object):

    def GetResourcePermissionItemIds(self, resourceCategory, resourceId):
        pass

    def GrantResourcePermission(self, resourceCategory, resourceId, grantPermissionItemIds):
        pass

    def RevokeResourcePermission(self, resourceCategory, resourceId, revokePermissionItemIds):
        pass

    def GetPermissionScopeTargetIds(self, resourceCategory, resourceId, targetCategory, permissionItemCode):
        pass

    def GetPermissionScopeResourceIds(self, resourceCategory, targetId, targetResourceCategory, permissionItemCode):
        pass

    def GrantPermissionScopeTargets(self, resourceCategory, resourceId, targetCategory, grantTargetIds, permissionItemId):
        pass

    def GrantPermissionScopeTarget(self, resourceCategory, resourceIds, targetCategory, grantTargetId, permissionItemId):
        pass

    def RevokePermissionScopeTargets(self, resourceCategory, resourceId, targetCategory, revokeTargetIds, permissionItemId):
        pass

    def RevokePermissionScopeTarget(self, resourceCategory, resourceIds, targetCategory, revokeTargetId, permissionItemId):
        pass

    def ClearPermissionScopeTarget(self, resourceCategory, resourceId, targetCategory, permissionItemId):
        pass

    def GetResourceScopeIds(self, userId, targetCategory, permissionItemCode):
        pass

    def GetTreeResourceScopeIds(self, userId, targetCategory, permissionItemCode, childrens):
        pass