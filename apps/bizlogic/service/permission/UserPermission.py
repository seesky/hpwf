# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2018/12/12 8:52'

from apps.bizlogic.models import Piuser
from apps.bizlogic.models import Piuserrole
from apps.bizlogic.models import Pipermission
from apps.bizlogic.models import Pipermissionscope
from apps.bizlogic.models import Pipermissionitem

from apps.bizlogic.service.base.SequenceService import SequenceService
from apps.bizlogic.service.base.PermissionScopeService import PermissionScopeService

from apps.utilities.message.PermissionScope import PermissionScope

from django.db.models import Q

class UserPermission(object):

    def GetUserPermissionItemIds(self, userId):
        """
          获取指定用户操作权限主键数组
          Args:
              userId (string): 用户主键
          Returns:
              returnValue(string[]): 操作权限主键数组
        """
        returnValue = Pipermission.objects.filter(Q(resourcecategory='PIUSER') & Q(deletemark=0) & Q(enabled=1) & Q(resourceid=userId)).values_list('permissionid', flat=True)
        return returnValue

    def GetUserIdsByPermissionItemId(self, permissionItemId):
        """
          获取用户主键数组通过指定操作权限
          Args:
              permissionItemId (string): 操作权限主键
          Returns:
              returnValue(string[]): 用户主键数组
        """
        returnValue = Pipermission.objects.filter(Q(resourcecategory='PIUSER') & Q(deletemark=0) & Q(enabled=1) & Q(permissionid=permissionItemId)).values_list('resourceid', flat=True)
        return returnValue

    def GrantUserPermissions(self, userIds, grantPermissionItemIds):
        """
          批量授予用户操作权限
          Args:
              userIds (string): 用户主键数组
              grantPermissionItemIds (string): 授予操作权限主键数组
          Returns:
              returnValue(int): 影响行数
        """
        returnValue = 0
        sequenceIds = SequenceService.GetBatchSequence(self, userIds.count() * grantPermissionItemIds.count())
        for i in range(userIds.count()):
            for j in range(grantPermissionItemIds.count()):
                UserPermission.Grant(self, sequenceIds[i * grantPermissionItemIds.count() + j], userIds[i], grantPermissionItemIds[j])
                returnValue = returnValue + 1
        return returnValue

    def GrantUserPermissionById(self, userId, grantPermissionItemId):
        """
          授予指定用户指定的操作权限
          Args:
              userId (string): 用户主键
              grantPermissionItemId (string): 授予操作权限主键
          Returns:
              returnValue(int): 影响的行数
        """
        returnValue = 0
        if grantPermissionItemId:
            returnValue = UserPermission.Grant(self, '', userId, grantPermissionItemId)
        return returnValue

    def RevokeUserPermissions(self, userIds, revokePermissionItemIds):
        """
          批量撤消用户的操作权限
          Args:
              userIds (string): 用户主键
              revokePermissionItemIds (string): 授予操作权限主键
          Returns:
              returnValue(int): 影响的行数
        """
        returnValue = 0
        if userIds & revokePermissionItemIds:
            for uid in userIds:
                for rid in revokePermissionItemIds:
                    returnValue = returnValue + UserPermission.Revoke(self, uid, rid)
        return returnValue

    def RevokeUserPermissionById(self, userId, revokePermissionItemId):
        """
          撤消指定用户指定的操作权限
          Args:
              userId (string): 用户主键
              revokePermissionItemId (string): 授予操作权限主键
          Returns:
              returnValue(int): 影响的行数
        """
        returnValue = 0
        returnValue = UserPermission.Revoke(self, userId, revokePermissionItemId)
        return returnValue

    def GetScopeOrganizeIdsByUserId(self, userId, permissionItemCode):
        """
          获取指定用户在某个权限域(或操作权限编号)下所拥有的组织机构主键数组
          如：指定用户可访问或管理那些组织机构数据
          Args:
              userId (string): 用户主键
              permissionItemCode (string): 操作权限编号
          Returns:
              returnValue(string[]): 组织机构主键数组
        """
        returnValue = PermissionScopeService.GetOrganizeIds(self, userId, permissionItemCode)
        return returnValue

    def GrantUserOrganizeScope(self, userId, permissionScopeItemCode, grantOrganizeIds):
        """
          授予用户的某个权限域的组织机构授权范围
          Args:
              userId (string): 用户主键
              permissionScopeItemCode (string): 操作权限编号
              grantOrganizeIds (string[]): 授予的组织主键数组
          Returns:
              returnValue(int): 影响的行数
        """
        returnValue = 0
        for id in grantOrganizeIds:
            UserPermission.GrantOrganize(self, userId, permissionScopeItemCode, id)
            returnValue = returnValue + 1
        return returnValue

    def RevokeUserOrganizeScope(self, userId, permissionScopeItemCode, revokeOrganizeIds):
        """
          撤消用户的某个权限域的组织组织授权范围
          Args:
              userId (string): 用户主键
              permissionScopeItemCode (string): 操作权限编号
              revokeOrganizeIds (string[]): 撤消的组织主键数组
          Returns:
              returnValue(int): 影响的行数
        """
        returnValue = 0
        for id in revokeOrganizeIds:
            UserPermission.RevokeOrganize(self, userId, permissionScopeItemCode, id)
            returnValue = returnValue + 1
        return returnValue

    def GetScopeUserIdsByUserId(self, userId, permissionItemCode):
        """
          获取指定用户在某个权限域下所有用户主键数组
          Args:
              userId (string): 用户主键
              permissionItemCode (string): 操作权限编号
          Returns:
              returnValue(string[]): 用户主键数组
        """
        returnValue = PermissionScopeService.GetUserIds(userId, permissionItemCode)
        return returnValue

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
        except Exception as e:
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

    def Grant(self, id, userId, permissionItemId):
        """
          为了提高授权的运行速度
          Args:
              id (string): 主键
              userIds (string): 用户主键
              permissionItemId (string): 权限主键
          Returns:
              returnValue(string): 主键
        """
        resourcePermissionEntity = Pipermission()
        resourcePermissionEntity.resourcecategory = 'PIUSER'
        resourcePermissionEntity.resourceid = userId
        resourcePermissionEntity.permissionid = permissionItemId
        resourcePermissionEntity.enabled = 1

        try:
            Pipermission.objects.get(Q(resourcecategory='PIUSER') & Q(resourceid=userId) & Q(permissionid=permissionItemId) & Q(deletemark=0))
            return ''
        except Pipermission.DoesNotExist as e:
            resourcePermissionEntity.save()
            return resourcePermissionEntity.id

    def Revoke(self, userId, permissionItemId):
        """
          为了提高撤销的运行速度
          Args:
              userId (string): 用户主键
              permissionItemId (string): 权限主键
          Returns:
              returnValue(string): 主键
        """
        returnValue = Pipermission.objects.filter(Q(resourcecategory='PIUSER') & Q(resourceid=userId) & Q(permissionid=permissionItemId)).delete()
        return returnValue

    def GrantOrganize(self, userId, permissionItemCode, grantOrganizeId):
        """
          为了提高授权的运行速度
          Args:
              userId (string): 员工主键
              permissionItemCode (string): 权限代码
              grantOrganizeId (string): 权限主键
          Returns:
              returnValue(string): 主键
        """
        returnValue = ''
        try:
            Pipermissionscope.objects.get(Q(resourcecategory='PIUSER') & Q(resourceid=userId) & Q(targetcategory='PIORGANIZE') & Q(targetid=grantOrganizeId) & Q(permissionid=Pipermissionitem.objects.get(code=permissionItemCode).id))
        except Pipermissionscope.DoesNotExist as e:
            resourcePermissionScopeEntity = Pipermissionscope()
            resourcePermissionScopeEntity.permissionid = Pipermissionitem.objects.get(code=permissionItemCode).id
            resourcePermissionScopeEntity.resourcecategory = 'PIUSER'
            resourcePermissionScopeEntity.resourceid = userId
            resourcePermissionScopeEntity.targetcategory = 'PIORGANIZE'
            resourcePermissionScopeEntity.targetid = grantOrganizeId
            resourcePermissionScopeEntity.enabled = 1
            resourcePermissionScopeEntity.deletemark = 0
            resourcePermissionScopeEntity.save()
            returnValue = resourcePermissionScopeEntity.id

            if grantOrganizeId != PermissionScope.PermissionScopeDic.get('No'):
                try:
                    dt = Pipermissionscope.objects.get(
                        Q(resourcecategory='PIUSER') & Q(resourceid=userId) & Q(targetcategory='PIORGANIZE') & Q(
                            targetid=PermissionScope.PermissionScopeDic.get('No')) & Q(
                            permissionid=Pipermissionitem.objects.get(code=permissionItemCode).id))
                    dt.delete()
                except Pipermissionscope.DoesNotExist as e:
                    pass
            else:
                dt = Pipermissionscope.objects.filter(Q(resourcecategory='PIUSER') & Q(resourceid=userId) & Q(targetcategory='PIORGANIZE')  &
                    Q(permissionid=Pipermissionitem.objects.get(code=permissionItemCode).id)).delete()
            return returnValue

    def RevokeOrganize(self, userId, permissionItemCode, revokeOrganizeId):
        """
          为了提高授权的运行速度
          Args:
              userId (string): 员工主键
              permissionItemCode (string): 权限代码
              revokeOrganizeId (string): 权限主键
          Returns:
              returnValue(string): 主键
        """
        returnValue = Pipermissionscope.objects.filter(Q(resourcecategory='PIUSER') & Q(resourceid=userId) & Q(targetcategory='PIORGANIZE') & Q(targetid=revokeOrganizeId) & Q(permissionid=Pipermissionitem.objects.get(code=permissionItemCode).id)).delete()
        return returnValue


