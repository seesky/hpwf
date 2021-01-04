# _*_ coding: utf-8 _*_
__author__ = 'baxuelong@163.com'
__date__ = '2018/12/12 8:21'

from apps.bizlogic.models import Pipermissionscope
from apps.bizlogic.models import Pipermissionitem
from apps.bizlogic.models import Pipermission

from django.db.models import Q

class OrganizePermission(object):

    def GetScopeModuleIdsByOrganizeId(self, organizeId, permissionItemCode):
        """
        获取指定组织机构在某个权限域下所有模块主键数组
        Args:
            organizeId (string): 组织机构主键
            permissionItemCode (string): 操作权限编号
        Returns:
            returnValue(string[]): 组织机构主键数组
        """
        returnValue = Pipermissionscope.objects.filter(Q(resourcecategory='PIORGANIZE') & Q(resourceid=organizeId) & Q(targetcategory='PIMODULE') & Q(permissionid=Pipermissionitem.objects.get(code=permissionItemCode).id)).values_list('targetid', flat=True)
        return returnValue

    def GrantOrganizeModuleScopes(self, organizeId, permissionItemCode, grantModuleIds):
        """
        授予组织机构某个权限域的模块授权范围
        Args:
            organizeId (string): 组织机构主键
            permissionItemCode (string): 操作权限编号
            grantModuleIds (string[]): 授予模块主键数组
        Returns:
            returnValue(int): 影响行数
        """
        returnValue = 0
        for id in grantModuleIds:
            resourcePermissionScopeEntity = Pipermissionscope()
            resourcePermissionScopeEntity.id = Pipermissionitem.objects.get(code=permissionItemCode).id
            resourcePermissionScopeEntity.resourcecategory = 'PIORGANIZE'
            resourcePermissionScopeEntity.resourceid = organizeId
            resourcePermissionScopeEntity.targetcategory = 'PIMODULE'
            resourcePermissionScopeEntity.targetid = id
            resourcePermissionScopeEntity.enabled = 1
            resourcePermissionScopeEntity.deletemark = 0
            resourcePermissionScopeEntity.save()
            returnValue = returnValue + 1
        return returnValue

    def GrantOrganizeModuleScope(self, organizeId, permissionItemCode, grantModuleId):
        """
        授予组织机构某个权限域的模块授权范围
        Args:
            organizeId (string): 组织机构主键
            permissionItemCode (string): 操作权限编号
            grantModuleId (string[]): 授予模块主键
        Returns:
            returnValue(int): 影响行数
        """
        returnValue = 0
        resourcePermissionScopeEntity = Pipermissionscope()
        resourcePermissionScopeEntity.id = Pipermissionitem.objects.get(code=permissionItemCode).id
        resourcePermissionScopeEntity.resourcecategory = 'PIORGANIZE'
        resourcePermissionScopeEntity.resourceid = organizeId
        resourcePermissionScopeEntity.targetcategory = 'PIMODULE'
        resourcePermissionScopeEntity.targetid = grantModuleId
        resourcePermissionScopeEntity.enabled = 1
        resourcePermissionScopeEntity.deletemark = 0
        resourcePermissionScopeEntity.save()
        returnValue = 1
        return returnValue

    def RevokeOrganizeModuleScopes(self, organizeId, permissionItemCode, revokeModuleIds):
        """
        撤消指定组织机构某个权限域的模块授权范围
        Args:
            organizeId (string): 组织机构主键
            permissionItemCode (string): 操作权限编号
            grantModuleIds (string[]): 授予模块主键列表
        Returns:
            returnValue(int): 影响行数
        """
        returnValue = 0

        returnValue = Pipermissionscope.objects.filter(Q(resourcecategory='PIORGANIZE') & Q(resourceid=organizeId) & Q(targetcategory='PIMODULE') & Q(targetid__in=revokeModuleIds) & Q(permissionid=Pipermissionitem.objects.get(code=permissionItemCode).id)).delete()
        return returnValue

    def RevokeOrganizeModuleScope(self, organizeId, permissionItemCode, revokeModuleId):
        """
        撤消指定组织机构某个权限域的模块授权范围
        Args:
            organizeId (string): 组织机构主键
            permissionItemCode (string): 操作权限编号
            grantModuleIds (string[]): 授予模块主键列表
        Returns:
            returnValue(int): 影响行数
        """
        returnValue = 0

        returnValue = Pipermissionscope.objects.filter(
            Q(resourcecategory='PIORGANIZE') & Q(resourceid=organizeId) & Q(targetcategory='PIMODULE') & Q(
                targetid=revokeModuleId) & Q(
                permissionid=Pipermissionitem.objects.get(code=permissionItemCode).id)).delete()
        return returnValue

    def GetOrganizePermissionItemIds(self, organizeId):
        """
        获取指定组织机构操作权限主键数组
        Args:
            organizeId (string): 组织机构主键
        Returns:
            returnValue(string[]): 主键数组
        """
        returnValue = None
        returnValue = Pipermission.objects.filter(Q(resourcecategory='PIORGANIZE') & Q(resourceid=organizeId) & Q(enabled=1) & Q(deletemark=0)).values_list('permissionid', flat=True)
        return returnValue

    def GetOrganizeIdsByPermissionItemId(self, permissionItemId):
        """
        获取组织机构主键数组通过指定操作权限
        Args:
            permissionItemId (string): 操作权限主键
        Returns:
            returnValue(string[]): 主键数组
        """
        returnValue = None
        returnValue = Pipermission.objects.filter(Q(resourcecategory='PIORGANIZE') & Q(permissionid=permissionItemId) & Q(enabled=1) & Q(deletemark=0)).values_list('resourceid', flat=True)
        return returnValue

    def GrantOrganizePermissions(self, organizeIds, grantPermissionItemIds):
        """
        授予组织机构操作权限
        Args:
            organizeIds (string): 组织机构主键数组
            grantPermissionItemIds (string): 授予操作权限主键数组
        Returns:
            returnValue(int): 影响行数
        """
        returnValue = 0
        for org in organizeIds:
            for item in grantPermissionItemIds:
                resourcePermission = Pipermission()
                resourcePermission.resourcecategory = 'PIORGANIZE'
                resourcePermission.resourceid = org
                resourcePermission.permissionid = item
                resourcePermission.enabled = 1
                resourcePermission.save()
                returnValue = returnValue + 1
        return returnValue

    def GrantOrganizePermissionById(self, organizeId, grantPermissionItemId):
        """
        授予组织机构操作权限
        Args:
            organizeId (string): 组织机构主键
            grantPermissionItemId (string): 授予操作权限主键
        Returns:
            returnValue(int): 影响行数
        """
        resourcePermission = Pipermission()
        resourcePermission.resourcecategory = 'PIORGANIZE'
        resourcePermission.resourceid = organizeId
        resourcePermission.permissionid = grantPermissionItemId
        resourcePermission.enabled = 1
        returnValue = resourcePermission.save()
        return returnValue

    def RevokeOrganizePermissions(self, organizeIds, revokePermissionItemIds):
        """
       撤消组织机构操作权限
       Args:
           organizeIds (string): 组织机构主键列表
           revokePermissionItemIds (string): 授予操作权限主键列表
       Returns:
           returnValue(int): 影响行数
       """
        returnValue = 0
        for org in organizeIds:
            for item in revokePermissionItemIds:
                Pipermission.objects.filter(Q(resourcecategory='PIORGANIZE') & Q(resourceid=org) & Q(permissionid=item)).delete()
                returnValue = returnValue + 1
        return returnValue

    def ClearOrganizePermission(self, organizeId):
        """
       清除组织机构权限
       1.清除组织机构的用户归属。
       2.清除组织机构的模块权限。
       3.清除组织机构的操作权限。
       Args:
           organizeId (string): 组织机构主键列表
       Returns:
           returnValue(int): 影响行数
       """
        returnValue = Pipermission.objects.filter(Q(resourcecategory='PIORGANIZE') & Q(resourceid=organizeId)).delete()
        returnValue = returnValue + Pipermissionscope.objects.filter(Q(resourcecategory='PIORGANIZE') & Q(resourceid=organizeId) & Q(permissionid=Pipermissionitem.objects.get(code='PIORGANIZE').id)).delete()
        return returnValue

    def RevokeOrganizePermissionById(self, organizeId, revokePermissionItemId):
        """
       撤消指定组织机构指定的操作权限
       Args:
           organizeId (string): 组织机构主键
           revokePermissionItemId (string): 授予操作权限主键
       Returns:
           returnValue(int): 影响行数
       """
        returnValue = Pipermission.objects.filter(Q(resourcecategory='PIORGANIZE') & Q(resourceid=organizeId) & Q(permissionid=revokePermissionItemId)).delete()
        return returnValue