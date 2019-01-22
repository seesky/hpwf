# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2018/12/12 8:27'

from apps.bizlogic.models import Pipermission
from apps.bizlogic.models import Pipermissionitem
from apps.bizlogic.models import Pipermissionscope
from apps.bizlogic.models import Piuser
from apps.bizlogic.models import Piuserrole

from apps.utilities.publiclibrary.SystemInfo import SystemInfo
from apps.utilities.message.PermissionScope import PermissionScope
from apps.utilities.publiclibrary.StringHelper import StringHelper
from apps.utilities.publiclibrary.DbCommonLibaray import DbCommonLibaray

import uuid

from django.db.models import Q

class ResourcePermission(object):

    def GetResourcePermissionItemIds(self, resourceCategory, resourceId):
        """
       获取资源权限主键数组
       Args:
           resourceCategory (string): 资源分类
           resourceId (string): 资源主键
       Returns:
           returnValue(string): 操作权限主键数组
       """
        returnValue = Pipermission.objects.filter(Q(resourcecategory=resourceCategory) & Q(resourceid=resourceId))
        return returnValue

    def GrantResourcePermission(self, resourceCategory, resourceId, grantPermissionItemIds):
        """
       授予资源的权限
       Args:
           resourceCategory (string): 资源分类
           resourceId (string): 资源主键
           grantPermissionItemIds (string): 操作权限主键列表
       Returns:
           returnValue(int): 影响行数
       """
        returnValue = 0
        if grantPermissionItemIds:
            for item in grantPermissionItemIds:
                resourcePermissionEntity = Pipermission()
                resourcePermissionEntity.resourcecategory = resourceCategory
                resourcePermissionEntity.permissionid = resourceId
                resourcePermissionEntity.permissionid = item
                resourcePermissionEntity.deletemark = 0
                resourcePermissionEntity.save()
                returnValue = returnValue + 1
        return returnValue

    def RevokeResourcePermission(self, resourceCategory, resourceId, revokePermissionItemIds):
        """
       授予资源的权限
       Args:
           resourceCategory (string): 资源分类
           resourceId (string): 资源主键
           revokePermissionItemIds (string): 操作权限主键列表
       Returns:
           returnValue(int): 影响行数
       """
        returnValue = 0
        if revokePermissionItemIds:
                returnValue = Pipermission.objects.filter(Q(resourcecategory=resourceCategory) & Q(resourceid=resourceId) & Q(permissionid__in=revokePermissionItemIds)).delete()
        return returnValue

    def GetPermissionScopeTargetIds(self, resourceCategory, resourceId, targetCategory, permissionItemCode):
        """
       获取资源权限范围主键数组
       Args:
           resourceCategory (string): 资源分类
           resourceId (string): 资源主键
           targetCategory (string): 目标类别
           permissionItemCode (string): 操作权限编号
       Returns:
           returnValue(string[]): 目标资源主键数组
       """
        try:
            permissionItemId = Pipermissionitem.objects.get(code=permissionItemCode).id
        except Pipermissionitem.DoesNotExist as e:
            permissionItemId = ''
        returnValue = Pipermissionscope.objects.filter(Q(resourcecategory=resourceCategory) & Q(resourceid=resourceId) & Q(permissionid=permissionItemId) & Q(targetcategory=targetCategory) & Q(deletemark=0) & Q(enabled=1)).values_list('targetid', flat=True)
        return returnValue

    def GetPermissionScopeResourceIds(self, resourceCategory, targetId, targetResourceCategory, permissionItemCode):
        """
       获取数据权限目标主键
       Args:
           resourceCategory (string): 资源分类
           targetId (string): 目标资源主键
           targetResourceCategory (string): 目标资源类别
           permissionItemCode (string): 操作权限编号
       Returns:
           returnValue(string[]): 资源主键数组
       """
        permissionItemId = Pipermissionitem.objects.get(code=permissionItemCode).id
        returnValue = Pipermissionscope.objects.filter(Q(resourcecategory=resourceCategory) & Q(targetid=targetId) & Q(permissionid=permissionItemId) & Q(targetcategory=targetResourceCategory) & Q(deletemark=0) & Q(enabled=1)).values_list('resourceid', flat=True)
        return returnValue

    def GrantPermissionScopeTargets(self, resourceCategory, resourceId, targetCategory, grantTargetIds, permissionItemId):
        """
       授予资源的权限范围
       Args:
           resourceCategory (string): 资源分类
           resourceId (string): 资源主键
           targetCategory (string): 目标类别
           grantTargetIds (string): 目标主键数组
           permissionItemId (string): 权限主键
       Returns:
           returnValue(int): 影响的行数
       """
        returnValue = 0
        for id in grantTargetIds:
            resourcePermissionScope = Pipermissionscope()
            resourcePermissionScope.id = None
            resourcePermissionScope.resourcecategory = resourceCategory
            resourcePermissionScope.resourceid = resourceId
            resourcePermissionScope.targetcategory = targetCategory
            resourcePermissionScope.permissionid = permissionItemId
            resourcePermissionScope.targetid = id
            resourcePermissionScope.startdate = None
            resourcePermissionScope.enabled = 1
            resourcePermissionScope.deletemark = 0

            try:
                Pipermissionscope.objects.get(Q(resourceid=resourceId) & Q(resourcecategory=resourceCategory) & Q(targetcategory=targetCategory) & Q(targetid=id) & Q(permissionid=permissionItemId) & Q(enabled=1) & Q(deletemark=0))
            except Pipermissionscope.DoesNotExist as e:
                resourcePermissionScope.save()
                returnValue = returnValue + 1
        return returnValue

    def GrantPermissionScopeTarget(self, resourceCategory, resourceId, targetCategory, grantTargetId, permissionItemId):
        """
       授予资源的权限范围
       Args:
           resourceCategory (string): 资源分类
           resourceId (string): 资源主键
           targetCategory (string): 目标类别
           grantTargetId (string): 目标主键数组
           permissionItemId (string): 权限主键
       Returns:
           returnValue(int): 影响的行数
       """
        returnValue = 0
        for id in grantTargetId:
            resourcePermissionScope = Pipermissionscope()
            resourcePermissionScope.id = uuid.uuid4()
            resourcePermissionScope.resourcecategory = resourceCategory
            resourcePermissionScope.resourceid = resourceId
            resourcePermissionScope.targetcategory = targetCategory
            resourcePermissionScope.permissionid = permissionItemId
            resourcePermissionScope.targetid = id
            resourcePermissionScope.enabled = 1
            resourcePermissionScope.deletemark = 0

            try:
                Pipermissionscope.objects.get(Q(resourceid=resourceId) & Q(resourcecategory=resourceCategory) & Q(
                    targetcategory=targetCategory) & Q(targetid=id) & Q(permissionid=permissionItemId) & Q(
                    enabled=1) & Q(deletemark=0))
            except Pipermissionscope.DoesNotExist as e:
                resourcePermissionScope.save()
                returnValue = returnValue + 1
        return returnValue


    def RevokePermissionScopeTargets(self, resourceCategory, resourceId, targetCategory, revokeTargetIds, permissionItemId):
        """
       撤消资源的权限范围
       Args:
           resourceCategory (string): 资源分类
           resourceId (string): 资源主键
           targetCategory (string): 目标类别
           revokeTargetIds (string): 目标主键数组
           permissionItemId (string): 权限主键
       Returns:
           returnValue(int): 影响的行数
       """
        returnValue = Pipermissionscope.objects.filter(Q(resourcecategory=resourceCategory) & Q(resourceid=resourceId) & Q(targetcategory=targetCategory) & Q(targetid__in=revokeTargetIds) & Q(permissionid=permissionItemId))
        return returnValue

    def RevokePermissionScopeTarget(self, resourceCategory, resourceIds, targetCategory, revokeTargetId, permissionItemId):
        """
       撤消资源的权限范围
       Args:
           resourceCategory (string): 资源分类
           resourceIds (string): 资源主键
           targetCategory (string): 目标类别
           revokeTargetId (string): 目标主键数组
           permissionItemId (string): 权限主键
       Returns:
           returnValue(int): 影响的行数
       """
        returnValue,r = Pipermissionscope.objects.filter(
            Q(resourcecategory=resourceCategory) & Q(resourceid=resourceIds) & Q(targetcategory=targetCategory) & Q(
                targetid__in=revokeTargetId) & Q(permissionid=permissionItemId)).delete()
        return returnValue

    def ClearPermissionScopeTarget(self, resourceCategory, resourceId, targetCategory, permissionItemId):
        """
       撤消资源的权限范围
       Args:
           resourceCategory (string): 资源分类
           resourceId (string): 资源主键
           targetCategory (string): 目标类别
           permissionItemId (string): 权限主键
       Returns:
           returnValue(int): 影响的行数
       """
        returnValue = Pipermissionscope.objects.filter(Q(resourcecategory=resourceCategory) & Q(resourceid=resourceId) & Q(targetcategory=targetCategory) & Q(permissionid=permissionItemId) & Q(enabled=1))
        return returnValue

    def GetResourceScopeIds(self, userId, targetCategory, permissionItemCode):
        """
       获取用户的某个资源的权限范围
       Args:
           userId (string): 用户主键
           targetCategory (string): 目标类别
           permissionItemCode (string): 权限编号
       Returns:
           returnValue(string[]): 主键数组
       """
        permissionItemId = Pipermissionitem.objects.get(code = permissionItemCode)
        defaultRoleId = Piuser.objects.get(id = userId).roleid


        '''
            // 用户的权限
                          " SELECT PIPERMISSIONSCOPE.TARGETID "
                        + "   FROM PIPERMISSIONSCOPE "
                        + "  WHERE (PIPERMISSIONSCOPE.RESOURCECATEGORY = '" + PiUserTable.TableName + "') "
                        + "        AND (PIPERMISSIONSCOPE.RESOURCEID = '" + userId + "') "
                        + "        AND (PIPERMISSIONSCOPE.TARGETCATEGORY = '" + targetCategory + "') "
                        + "        AND (PIPERMISSIONSCOPE.PERMISSIONID = '" + permissionItemId + "') "
                        + "        AND (PIPERMISSIONSCOPE.ENABLED = 1) "
                        + "        AND (PIPERMISSIONSCOPE.DELETEMARK = 0) "
                        //+ "        AND (dbo.PiPermissionScope.TargetId IN ( "
                        //+ "             SELECT PiModule.Id FROM PiModule WHERE DeleteMark = 0 AND Enabled = 1 )) "
                      
                        + " UNION "
               
                        // 用户归属的角色的权限                            
                        + " SELECT PIPERMISSIONSCOPE.TARGETID "
                        + "   FROM PIPERMISSIONSCOPE "
                        + "  WHERE (PIPERMISSIONSCOPE.RESOURCECATEGORY  = '" + PiRoleTable.TableName + "') "
                        + "        AND (PIPERMISSIONSCOPE.TARGETCATEGORY  = '" + targetCategory + "') "
                        + "        AND (PIPERMISSIONSCOPE.PERMISSIONID = '" + permissionItemId + "') "
                        + "        AND (PIPERMISSIONSCOPE.DELETEMARK = 0)"
                        + "        AND (PIPERMISSIONSCOPE.ENABLED = 1) "
                        + "        AND ((PIPERMISSIONSCOPE.RESOURCEID IN ( "
                        + "             SELECT PIUSERROLE.ROLEID "
                        + "               FROM PIUSERROLE "
                        + "              WHERE (PIUSERROLE.USERID  = '" + userId + "') "
                        + "                  AND (PIUSERROLE.ENABLED = 1) "
                        + "                  AND (PIUSERROLE.DELETEMARK = 0) ) ";
                        if (!string.IsNullOrEmpty(defaultRoleId))
                        {
                            // 用户的默认角色
                            sqlQuery += " OR (PIPERMISSIONSCOPE.RESOURCEID = '" + defaultRoleId + "')";
                        }
                        sqlQuery += " ) " 
                        + " ) ";
        
        '''
        q1 = Pipermissionscope.objects.filter(Q(resourcecategory='PIUSER') & Q(resourceid=userId) & Q(targetcategory=targetCategory) & Q(permissionid=permissionItemId) & Q(enabled=1) & Q(deletemark=0)).values_list('targetid', flat=True)
        if defaultRoleId:
            q2 = Pipermissionscope.objects.filter(Q(resourcecategory='PIROLE') & Q(targetcategory=targetCategory) & Q(permissionid=permissionItemId) & Q(deletemark=0) & Q(enabled=1) & Q(resourceid__in=Piuserrole.objects.filter(Q(userid=userId) & Q(enabled=1) & Q(deletemark=0)).values_list('roleid', flat=True))).values_list('targetid', flat=True)
        else:
            q2 = Pipermissionscope.objects.filter(
                Q(resourcecategory='PIROLE') & Q(targetcategory=targetCategory) & Q(permissionid=permissionItemId) & Q(
                    deletemark=0) & Q(enabled=1) & (Q(resourceid__in=Piuserrole.objects.filter(
                    Q(userid=userId) & Q(enabled=1) & Q(deletemark=0)).values_list('roleid', flat=True)) | Q(resourceid=defaultRoleId) )).values_list('targetid', flat=True)

        resourceIds = q1.union(q2)

        if SystemInfo.EnableOrganizePermission:
            userEntity = Piuser.objects.get(id=userId)
            resourceIdsByOrganize = Pipermissionscope.objects.filter(Q(resourcecategory='PIORGANIZE') & (Q(resourceid=userEntity.companyid) | Q(resourceid=userEntity.departmentid) |Q(resourceid=userEntity.workgroupid)) & Q(targetcategory=targetCategory) & Q(permissionid=permissionItemId) & Q(enabled=1) & Q(deletemark=0)).values_list('targetid', flat=True)
            resourceIds = resourceIds.union(resourceIdsByOrganize)

        if targetCategory == 'PIORGANIZE':
            permissionScope,resourceIds = ResourcePermission.TransformPermissionScope(self, userId, resourceIds)

        return resourceIds

    def TransformPermissionScope(self, userId, resourceIds):
        """
      转换用户的权限范围
      Args:
          userId (string): 用户主键
          resourceIds (string): 权限范围
      Returns:
          returnValue(Pipermissionscop):
      """
        permissionScope = PermissionScope.PermissionScopeDic.get('No')
        if resourceIds and resourceIds.count() > 0:
            userEntity = Piuser.objects.get(id=userId)

            for id in resourceIds:
                if id ==  PermissionScope.PermissionScopeDic.get('All'):
                    continue
                if id ==  PermissionScope.PermissionScopeDic.get('UserCompany'):
                    id = userEntity.companyid
                    permissionScope =  PermissionScope.PermissionScopeDic.get('UserCompany')
                    continue
                if id ==  PermissionScope.PermissionScopeDic.get('UserDepartment'):
                    id = userEntity.departmentid
                    permissionScope = PermissionScope.PermissionScopeDic.get('UserDepartment')
                    continue
                if id ==  PermissionScope.PermissionScopeDic.get('UserWorkgroup'):
                    id = userEntity.workgroupid
                    permissionScope = PermissionScope.PermissionScopeDic.get('UserWorkgroup')
                    continue
        return permissionScope, resourceIds


    def GetTreeResourceScopeIds(self, userId, targetCategory, permissionItemCode, childrens):
        """
      树型资源的权限范围
      Args:
          userId (string): 用户主键
          targetCategory (string): 资源分类
          permissionItemCode (权限编号):
          childrens (是否含子节点):
      Returns:
          returnValue(string[]): 主键数组
      """
        resourceScopeIds = ResourcePermission.GetResourceScopeIds(self, userId, targetCategory, permissionItemCode)
        isList = StringHelper.ArrayToList(self, resourceScopeIds, ',')
        if not childrens:
            return resourceScopeIds

        if resourceScopeIds:
            sqlQuery = "SELECT ID FROM (SELECT ID  FROM " + targetCategory + " WHERE (Id IN (" + isList + ") ) UNION ALL SELECT ResourceTree.Id AS ID FROM " + targetCategory + " AS ResourceTree INNER JOIN  PiPermissionScope AS A ON A.Id = ResourceTree.ParentId) AS PermissionScopeTree"
            resourceIds = DbCommonLibaray.executeQuery(self, sqlQuery)
            #TODO:这里有一个BUG
            return resourceScopeIds.Concat(resourceIds)

        return resourceScopeIds

