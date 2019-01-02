# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2018/12/12 8:36'

from apps.bizlogic.models import Pipermission
from apps.bizlogic.models import Pirole
from apps.bizlogic.models import Pipermissionitem
from apps.bizlogic.models import Pipermissionscope

from apps.utilities.message.PermissionScope import PermissionScope

from apps.bizlogic.service.base.UserRoleService import UserRoleService

from django.db.models import Q

class RolePermission(object):

    def GetRolePermissionItemIds(self, roleId):
        """
      获取指定角色操作权限主键数组
      Args:
          roleId (string): 角色主键
      Returns:
          returnValue(string[]): 主键数组
      """
        returnValue = Pipermission.objects.filter(Q(resourcecategory='PIROLE') & Q(deletemark=0) & Q(enabled=1) & Q(resourceid=roleId))
        return returnValue

    def GetRoleIdsByPermissionItemId(self, permissionItemId):
        """
      获取角色主键数组通过指定操作权限
      Args:
          permissionItemId (string): 操作权限主键
      Returns:
          returnValue(string[]): 主键数组
      """
        returnValue = Pipermission.objects.filter(Q(resourcecategory='PIROLE') & Q(deletemark=0) & Q(enabled=1) & Q(permissionid=permissionItemId))
        return returnValue

    def GrantRolePermissions(self, roleIds, grantPermissionItemIds):
        """
      批量授予角色的操作权限
      Args:
          roleIds (string[]): 角色主键数组
          grantPermissionItemIds (string[]): 授予操作权限主键数组
      Returns:
          returnValue(int): 影响行数
      """
        returnValue = 0
        for roleid in roleIds:
            for pItemId in grantPermissionItemIds:
                RolePermission.Grant(self, roleid, pItemId)
                returnValue = returnValue + 1
        return returnValue

    def GrantRolePermission(self, roleName, permissionItemCode):
        """
      授予指定角色指定的操作权限
      Args:
          roleName (string): 角色名
          permissionItemCode (string): 权限编号
      Returns:
          returnValue(string): 主键
      """
        roleId = Pirole.objects.filter(realname=roleName).id
        permissionItemId = Pipermissionitem.objects.get(code=permissionItemCode).id
        returnValue = RolePermission.Grant(self, roleId, permissionItemId)
        return returnValue

    def GrantRolePermissionById(self, roleId, grantPermissionItemId):
        """
      授予指定角色特定的操作权限
      Args:
          roleId (string): 角色主键
          grantPermissionItemId (string): 权限主键
      Returns:
          returnValue(int): 影响行数
      """
        returnValue = RolePermission.Grant(self, roleId, grantPermissionItemId)
        return returnValue

    def RevokeRolePermissions(self, roleIds, revokePermissionItemIds):
        """
          撤销权限
          Args:
              roleId (string[]): 角色主键数组
              permissionItemId (string[]): 权限主键数组
          Returns:
              returnValue(string): 影响行数
        """
        returnValue = 0
        for roleid in roleIds:
            for permissionItemId in revokePermissionItemIds:
                returnValue = returnValue + RolePermission.Revoke(self, roleid, permissionItemId)
        return returnValue

    def RevokeRolePermission(self, roleName, permissionItemCode):
        """
          授予指定角色撤销的操作权限
          Args:
              roleName (string): 角色名
              permissionItemCode (string): 权限编号
          Returns:
              returnValue(string): 影响行数
        """
        roleId = Pirole.objects.filter(realname=roleName).id
        permissionItemId = Pipermissionitem.objects.get(code=permissionItemCode).id
        returnValue = RolePermission.Revoke(self, roleId, permissionItemId)
        return returnValue

    def RevokeRolePermissionById(self, roleId, revokePermissionItemId):
        """
          撤销权限
          Args:
              roleId (string[]): 角色主键数组
              permissionItemId (string[]): 权限主键数组
          Returns:
              returnValue(string): 影响行数
        """
        returnValue = RolePermission.Revoke(self, roleId, revokePermissionItemId)
        return returnValue

    def GetScopeUserIdsByRoleId(self, roleId, permissionItemCode):
        """
          获取指定角色在某个权限域(或操作权限编号)下所拥有的用户主键数组
          Args:
              roleId (string): 角色主键
              permissionItemCode (string): 操作权限编号
          Returns:
              returnValue(string[]): 用户主键数组
        """
        returnValue = Pipermissionscope.objects.filter(Q(resourcecategory='PIROLE') & Q(resourceid=roleId) & Q(targetcategory='PIUSER') & Q(permissionid=permissionItemCode)).values_list('targetid', flat=True)
        return returnValue

    def GetScopeRoleIdsByRoleId(self, roleId, permissionItemCode):
        """
          获取指定角色在某个权限域(或操作权限编号)下所拥有的角色主键数组
          Args:
              roleId (string): 角色主键
              permissionItemCode (string): 操作权限编号
          Returns:
              returnValue(string[]): 用户主键数组
        """
        returnValue = Pipermissionscope.objects.filter(
            Q(resourcecategory='PIROLE') & Q(resourceid=roleId) & Q(targetcategory='PIROLE') & Q(
                permissionid=permissionItemCode)).values_list('targetid', flat=True)
        return returnValue

    def GetScopeOrganizeIdsByRoleId(self, roleId, permissionItemCode):
        """
          获取指定角色在某个权限域(或操作权限编号)下所拥有的组织机构主键数组
          Args:
              roleId (string): 角色主键
              permissionItemCode (string): 操作权限编号
          Returns:
              returnValue(string[]): 用户主键数组
        """
        returnValue = Pipermissionscope.objects.filter(Q(resourcecategory='PIROLE') & Q(resourceid=roleId) & Q(targetcategory='PIORGANIZE') & Q(permissionid=permissionItemCode)).values_list('targetid', flat=True)
        return returnValue

    def GrantRoleUserScope(self, roleId, permissionItemCode, grantUserIds):
        """
          授予角色某个权限域的用户范围
          Args:
              roleId (string): 角色主键
              permissionItemCode (string): 操作权限编号
              grantUserIds (string): 授予用户主键数组
          Returns:
              returnValue(int): 影响行数
        """
        returnValue = 0
        for id in grantUserIds:
            RolePermission.GrantUser(self, roleId, permissionItemCode, id)
            returnValue = returnValue + 1
        return returnValue

    def RevokeRoleUserScope(self, roleId, permissionItemId, revokeUserIds):
        """
          撤消角色的某个权限域的用户范围
          Args:
              roleId (string): 角色主键
              permissionItemId (string): 操作权限主键
              revokeUserIds (string): 撤消的用户主键数组
          Returns:
              returnValue(int): 影响行数
        """
        returnValue =  0
        for id in revokeUserIds:
            RolePermission.RevokeUser(self, roleId, permissionItemId, id)
            returnValue = returnValue + 1
        return returnValue

    def GrantRoleRoleScope(self, roleId, permissionItemCode, grantRoleIds):
        """
          授予角色的某个权限域的角色范围
          Args:
              roleId (string): 角色主键
              permissionItemCode (string): 操作权限编号
              grantRoleIds (string): 授予角色主键数组
          Returns:
              returnValue(int): 影响行数
        """
        returnValue = 0
        for id in grantRoleIds:
            RolePermission.GrantRole(self, roleId, permissionItemCode, id)
            returnValue = returnValue + 1
        return returnValue

    def RevokeRoleRoleScope(self, roleId, permissionItemId, revokeRoleIds):
        """
          撤消角色的某个权限域的角色范围
          Args:
              roleId (string): 角色主键
              permissionItemId (string): 操作权限主键
              revokeRoleIds (string): 撤消的角色主键数组
          Returns:
              returnValue(int): 影响行数
        """
        returnValue = 0
        for id in revokeRoleIds:
            RolePermission.RevokeRole(self, roleId, permissionItemId, id)
            returnValue = returnValue + 1
        return returnValue

    def GrantRoleOrganizeScope(self, roleId, permissionItemCode, grantOrganizeIds):
        """
          授予角色的某个权限域的组织范围
          Args:
              roleId (string): 角色主键
              permissionItemId (string): 操作权限主键
              grantOrganizeIds (stringp[]): 授予组织主键数组
          Returns:
              returnValue(int): 影响行数
        """
        returnValue = 0
        for id in grantOrganizeIds:
            RolePermission.GrantOrganize(self, roleId, permissionItemCode, id)
            returnValue = returnValue + 1
        return returnValue

    def RevokeRoleOrganizeScope(self, roleId, permissionItemId, revokeOrganizeIds):
        """
          撤消角色的某个权限域的组织范围
          Args:
              roleId (string): 角色主键
              permissionItemId (string): 操作权限主键
              revokeOrganizeIds (stringp[]): 撤消的组织主键数组
          Returns:
              returnValue(int): 影响行数
        """
        returnValue = 0
        for id in revokeOrganizeIds:
            RolePermission.RevokeOrganize(self, roleId, permissionItemId, id)
            returnValue = returnValue + 1
        return returnValue

    def GetScopePermissionItemIdsByRoleId(self, roleId, permissionItemCode):
        """
          获取指定角色在某个权限域下所有操作（功能）权限主键数组
          Args:
              roleId (string): 角色主键
              permissionItemCode (string): 操作权限编号
          Returns:
              returnValue(string[]): 操作权限主键数组
        """
        returnValue = Pipermissionscope.objects.filter(Q(resourcecategory='PIROLE') & Q(resourceid=roleId) & Q(targetcategory='PIPERMISSIONITEM') & Q(permissionid=permissionItemCode)).values_list('targetid', flat=True)
        return returnValue


    def GrantRolePermissionItemScope(self, roleId, permissionItemCode, grantPermissionItemIds):
        """
          授予角色某个权限域的操作权限授权范围
          Args:
              roleId (string): 角色主键
              permissionItemCode (string): 操作权限编号
              grantPermissionItemIds (string[]): 授予的操作权限主键数组
          Returns:
              returnValue(int): 影响的行数
        """
        returnValue = 0
        for id in grantPermissionItemIds:
            RolePermission.GrantPermissionItem(self, roleId, permissionItemCode, id)
            returnValue = returnValue + 1
        return returnValue

    def RevokeRolePermissionItemScope(self, roleId, permissionItemCode, revokePermissionItemIds):
        """
          撤消指定角色某个权限域的操作权限授权范围
          Args:
              roleId (string): 角色主键
              permissionItemCode (string): 操作权限编号
              revokePermissionItemIds (string[]): 撤消的操作权限主键数组
          Returns:
              returnValue(int): 影响的行数
        """
        returnValue = 0
        for id in revokePermissionItemIds:
            RolePermission.RevokePermissionItem(self, roleId, permissionItemCode, id)
            returnValue = returnValue + 1
        return returnValue

    def ClearRolePermissionScope(self, roleId, permissionItemCode):
        """
          清除指定角色所有权限范围
          Args:
              roleId (string): 角色主键
              permissionItemCode (string): 操作权限编号
          Returns:
              returnValue(int): 影响的行数
        """
        returnValue = Pipermissionscope.objects.filter(Q(resourcecategory='PIROLE') & Q(resourceid=roleId) & Q(permissionid=Pipermissionitem.objects.get(code=permissionItemCode).id)).delete()
        return returnValue

    def ClearRolePermissionByRoleId(self, roleId):
        """
          清除指定角色的所有权限
          1.清除角色的用户归属。
          2.清除角色的模块权限。
          3.清除角色的操作权限。
          Args:
              roleId (string): 角色主键
          Returns:
              returnValue(int): 影响的行数
        """
        returnValue = 0
        returnValue = returnValue + UserRoleService.EliminateRoleUser(self, roleId)

        returnValue = returnValue + Pipermissionscope.objects.filter(Q(resourcecategory='PIROLE') & Q(resourceid=roleId)).delete()

        returnValue = returnValue + Pipermission.objects.filter(Q(resourcecategory='PIROLE') & Q(resourceid=roleId)).delete()

        return returnValue

    def GetScopeModuleIdsByRoleId(self, roleId, permissionItemCode):
        """
          获取指定角色在某个权限域下所有模块主键数组
          Args:
              roleId (string): 角色主键
              permissionItemCode (string): 操作权限编号
          Returns:
              returnValue(string[]): 模块主键数组
        """
        returnValue = Pipermissionscope.objects.filter(Q(resourcecategory='PIROLE') & Q(resourceid=roleId) & Q(targetcategory='PIMODULE') & Q(permissionid=Pipermissionitem.objects.get(code=permissionItemCode).id)).values_list('targetid', flat=True)
        return returnValue

    def GrantRoleModuleScope(self, roleId, permissionItemCode, grantModuleIds):
        """
          授予角色某个权限域的模块授权范围
          Args:
              roleId (string): 角色主键
              permissionItemCode (string): 操作权限编号
              grantModuleIds (string): 授予模块主键数组
          Returns:
              returnValue(int): 影响行数
        """
        returnValue = 0
        for id in grantModuleIds:
            RolePermission.GrantModule(self, roleId, permissionItemCode, id)
            returnValue = returnValue + 1
        return returnValue

    def RevokeRoleModuleScope(self, roleId, permissionItemCode, revokeModuleIds):
        """
          撤消指定角色某个权限域的模块授权范围
          Args:
              roleId (string): 角色主键
              permissionItemCode (string): 操作权限编号
              revokeModuleIds (string): 授予模块主键数组
          Returns:
              returnValue(int): 影响行数
        """
        returnValue = 0
        for id in revokeModuleIds:
            RolePermission.RevokeModule(self, roleId, permissionItemCode, id)
            returnValue = returnValue + 1
        return returnValue

    def Grant(self, roleId, permissionItemId):
        """
          授予指定角色指定的操作权限
          Args:
              roleId (string): 角色主键
              permissionItemId (string): 权限主键
          Returns:
              returnValue(string): 主键
        """
        try:
            Pipermission.objects.get(
                Q(resourcecategory='PIROLE') & Q(resourceid=roleId) & Q(permissionid=permissionItemId) & Q(
                    deletemark=0))
            returnValue = 0
            return returnValue
        except Pipermission.DoesNotExist as e:
            resourcePermission = Pipermission()
            resourcePermission.resourcecategory = 'PIROLE'
            resourcePermission.resourceid = roleId
            resourcePermission.permissionid = permissionItemId
            resourcePermission.enabled = 1
            resourcePermission.save()
            returnValue = 1
            return returnValue

    def Revoke(self, roleId, permissionItemId):
        """
          撤销权限
          Args:
              roleId (string): 角色主键
              permissionItemId (string): 权限主键
          Returns:
              returnValue(string): 影响行数
        """
        returnValue = Pipermission.objects.filter(Q(resourcecategory='PIROLE') & Q(resourceid=roleId) & Q(permissionid=permissionItemId)).delete()
        return returnValue

    def GrantUser(self, roleId, permissionItemCode, grantUserId):
        """
          为了提高授权的运行速度
          Args:
              roleId (string): 角色主键
              permissionItemCode (string): 权限代码
              grantUserId (string): 权限主键
          Returns:
              returnValue(string): 主键
        """
        resourcePermissionScopeEntity = Pipermissionscope()
        resourcePermissionScopeEntity.permissionid = Pipermissionitem.objects.get(code=permissionItemCode).id
        resourcePermissionScopeEntity.resourcecategory = 'PIROLE'
        resourcePermissionScopeEntity.resourceid = roleId
        resourcePermissionScopeEntity.targetcategory = 'PIUSER'
        resourcePermissionScopeEntity.targetid = grantUserId
        resourcePermissionScopeEntity.enabled = 1
        resourcePermissionScopeEntity.deletemark = 0
        resourcePermissionScopeEntity.save()
        return resourcePermissionScopeEntity.id

    def RevokeUser(self, roleId, permissionItemCode, revokeUserId):
        """
          为了提高授权的运行速度
          Args:
              roleId (string): 角色主键
              permissionItemCode (string): 权限代码
              revokeUserId (string): 权限主键
          Returns:
              returnValue(string): 主键
        """
        returnValue = Pipermissionscope.objects.filter(Q(resourcecategory='PIROLE') & Q(resourceid=roleId) & Q(targetcategory='PIUSER') & Q(targetid=revokeUserId) & Q(permissionid=Pipermissionitem.objects.get(code=permissionItemCode).id)).delete()
        return returnValue

    def GrantRole(self, roleId, permissionItemCode, grantRoleId):
        """
          为了提高授权的运行速度
          Args:
              roleId (string): 角色主键
              permissionItemCode (string): 权限代码
              revokeUserId (string): 权限主键
          Returns:
              returnValue(string): 主键
        """
        resourcePermissionScopeEntity = Pipermissionscope()
        resourcePermissionScopeEntity.permissionid = Pipermissionitem.objects.get(code=permissionItemCode)
        resourcePermissionScopeEntity.resourcecategory = 'PIROLE'
        resourcePermissionScopeEntity.resourceid = roleId
        resourcePermissionScopeEntity.targetcategory = 'PIROLE'
        resourcePermissionScopeEntity.targetid = grantRoleId
        resourcePermissionScopeEntity.enabled = 1
        resourcePermissionScopeEntity.deletemark = 0
        resourcePermissionScopeEntity.save()
        return resourcePermissionScopeEntity.id

    def RevokeRole(self, roleId, permissionItemCode, revokeRoleId):
        """
          为了提高授权的运行速度
          Args:
              roleId (string): 角色主键
              permissionItemCode (string): 权限代码
              revokeUserId (string): 权限主键
          Returns:
              returnValue(string): 主键
        """
        returnValue = Pipermissionscope.objects.filter(Q(resourcecategory='PIROLE') & Q(resourceid=roleId) & Q(targetcategory='PIROLE') & Q(targetid=revokeRoleId) & Q(permissionid=Pipermissionitem.objects.get(code=permissionItemCode).id)).delete()
        return returnValue

    def GrantOrganize(self, roleId, permissionItemCode, grantOrganizeId):
        """
          为了提高授权的运行速度
          Args:
              roleId (string): 角色主键
              permissionItemCode (string): 权限代码
              grantOrganizeId (string): 权限主键
          Returns:
              returnValue(string): 主键
        """
        returnValue = ''
        try:
            Pipermissionscope.objects.get(Q(resourcecategory='PIROLE') & Q(resourceid=roleId) & Q(targetcategory='PIORGANIZE') & Q(targetid = grantOrganizeId) & Q(permissionid=Pipermissionitem.objects.get(code=permissionItemCode).id))
            return returnValue
        except Pipermissionscope.DoesNotExist as e:
            resourcePermissionScopeEntity = Pipermissionscope()
            resourcePermissionScopeEntity.permissionid = Pipermissionitem.objects.get(code=permissionItemCode).id
            resourcePermissionScopeEntity.resourcecategory = 'PIROLE'
            resourcePermissionScopeEntity.resourceid = roleId
            resourcePermissionScopeEntity.targetcategory = 'PIORGANIZE'
            resourcePermissionScopeEntity.targetid = grantOrganizeId
            resourcePermissionScopeEntity.enabled = 1
            resourcePermissionScopeEntity.deletemark = 0
            resourcePermissionScopeEntity.save()
            returnValue = resourcePermissionScopeEntity.id

            if not grantOrganizeId == PermissionScope.PermissionScopeDic.get('No'):
                Pipermissionscope.objects.filter(Q(resourcecategory='PIROLE') & Q(resourceid=roleId) & Q(targetcategory='PIORGANIZE') & Q(
                            targetid=PermissionScope.PermissionScopeDic.get('No')) & Q(
                            permissionid=Pipermissionitem.objects.get(code=permissionItemCode).id)).delete()
            else:
                Pipermissionscope.objects.filter(Q(resourcecategory='PIROLE') & Q(resourceid=roleId) & Q(targetcategory='PIORGANIZE') & Q(
                            permissionid=Pipermissionitem.objects.get(code=permissionItemCode).id) & ~Q(targetid = PermissionScope.PermissionScopeDic.get('No'))).delete()
            return returnValue

    def RevokeOrganize(self, roleId, permissionItemCode, revokeOrganizeId):
        """
          为了提高授权的运行速度
          Args:
              roleId (string): 角色主键
              permissionItemCode (string): 权限代码
              revokeOrganizeId (string): 权限主键
          Returns:
              returnValue(string): 主键
        """
        returnValue = Pipermissionscope.objects.filter(Q(resourcecategory='PIROLE') & Q(resourceid=roleId) & Q(targetcategory='PIORGANIZE') & Q(targetid=revokeOrganizeId) & Q(permissionid=Pipermissionitem.objects.get(code=permissionItemCode).id)).delete()
        return returnValue

    def GrantPermissionItem(self, roleId, permissionItemCode, grantPermissionId):
        """
          为了提高授权的运行速度
          Args:
              roleId (string): 角色主键
              permissionItemCode (string): 权限代码
              grantPermissionId (string): 权限主键
          Returns:
              returnValue(string): 主键
        """
        resourcePermissionScopeEntity = Pipermissionscope()
        resourcePermissionScopeEntity.permissionid = Pipermissionitem.objects.get(code=permissionItemCode).id
        resourcePermissionScopeEntity.resourcecategory = 'PIROLE'
        resourcePermissionScopeEntity.resourceid = roleId
        resourcePermissionScopeEntity.targetcategory = 'PIPERMISSIONITEM'
        resourcePermissionScopeEntity.targetid = grantPermissionId
        resourcePermissionScopeEntity.enabled = 1
        resourcePermissionScopeEntity.deletemark = 0
        resourcePermissionScopeEntity.save()
        return resourcePermissionScopeEntity.id

    def RevokePermissionItem(self, roleId, permissionItemCode, revokePermissionId):
        """
          为了提高授权的运行速度
          Args:
              roleId (string): 角色主键
              permissionItemCode (string): 权限代码
              revokePermissionId (string): 权限主键
          Returns:
              returnValue(string): 主键
        """
        returnValue = Pipermissionscope.objects.filter(Q(resourcecategory='PIROLE') & Q(resourceid=roleId) & Q(targetcategory='PIPERMISSIONITEM') & Q(targetid=revokePermissionId) & Q(permissionid=Pipermissionitem.objects.get(code=permissionItemCode).id))
        return returnValue

    def GrantModule(self, roleId, permissionItemCode, grantModuleId):
        """
          为了提高授权的运行速度
          Args:
              roleId (string): 角色主键
              permissionItemCode (string): 权限代码
              grantModuleId (string): 模块权限主键
          Returns:
              returnValue(string): 主键
        """
        resourcePermissionScopeEntity = Pipermissionscope()
        resourcePermissionScopeEntity.permissionid = Pipermissionitem.objects.get(code=permissionItemCode)
        resourcePermissionScopeEntity.resourceid = roleId
        resourcePermissionScopeEntity.resourcecategory = 'PIROLE'
        resourcePermissionScopeEntity.targetcategory = 'PIMODULE'
        resourcePermissionScopeEntity.targetid = grantModuleId
        resourcePermissionScopeEntity.enabled = 1
        resourcePermissionScopeEntity.deletemark = 0
        resourcePermissionScopeEntity.save()
        return resourcePermissionScopeEntity.id

    def RevokeModule(self, roleId, permissionItemCode, revokeModuleId):
        """
          为了提高授权的运行速度
          Args:
              roleId (string): 角色主键
              permissionItemCode (string): 权限代码
              revokeModuleId (string): 模块权限主键
          Returns:
              returnValue(string): 主键
        """
        returnValue = Pipermissionscope.objects.filter(Q(resourcecategory='PIROLE') & Q(resourceid=roleId) & Q(targetcategory='PIMODULE') & Q(targetid=revokeModuleId) & Q(Pipermissionitem.objects.get(code=permissionItemCode).id)).delete()
        return returnValue

