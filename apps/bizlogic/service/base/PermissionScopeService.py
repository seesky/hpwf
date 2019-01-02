# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2018/12/19 16:02'

from apps.bizlogic.models import Pipermissionitem
from apps.bizlogic.models import Pipermissionscope
from apps.bizlogic.models import Piuser
from apps.bizlogic.models import Piuserrole

from apps.utilities.message.PermissionScope import PermissionScope
from apps.utilities.publiclibrary.StringHelper import StringHelper
from apps.utilities.publiclibrary.DbCommonLibaray import DbCommonLibaray

from django.db.models import Q

class PermissionScopeService(object):
    def GetTreeResourceScopeIds(self, userId, tableName, permissionItemCode, childrens):
        """
        用户名是否重复
        Args:
            fieldNames (string): 字段名
            fieldValue (string): 字段值
        Returns:
            returnValue(bool): 已存在
        """
        resourceScopeIds = None
        resourceScopeIds = PermissionScopeService.GetResourceScopeIds(self, userId, tableName, permissionItemCode)

        idList = StringHelper.ArrayToList(self, resourceScopeIds, '\'')

        if idList:
            sqlQuery = 'select id from ( select id from ' + tableName + ' where (id in (' + idList + ')) UNION ALL select ResourceTree.Id AS ID FROM ' + tableName + ' AS ResourceTree INNER JOIN pipermissionscope AS A ON A.Id = ResourceTree.ParentId) AS PermissionScopeTree'
            dataTable = DbCommonLibaray.executeQuery(self, sqlQuery)
        return resourceScopeIds

    def GetResourceScopeIds(self, userId, targetCategory, permissionItemCode):
        """
        获得用户的某个权限范围资源主键数组
        Args:
            userId (string): 用户主键
            targetCategory (string): 资源分类
            permissionItemCode (string): 权限编号
        Returns:
            returnValue(string[]): 主键数组
        """
        permissionItemId = Pipermissionitem.objects.get(code=permissionItemCode).id
        defaultRoleId = Piuser.objects.get(id=userId).roleid

        q1 = Pipermissionscope.objects.filter(Q(resourcecategory='PIUSER') & Q(resourceid=userId) & Q(targetcategory=targetCategory) & Q(permissionid=permissionItemId) & Q(enabled=1) & Q(deletemark=0)).values_list('targetid', flat=True)
        q2 = Pipermissionscope.objects.filter(Q(resourcecategory='PIROLE') & Q(resourcecategory=targetCategory) & Q(permissionid=permissionItemId) & Q(deletemark=0) & Q(enabled=1) & Q(resourceid__in=Piuserrole.objects.filter(Q(userid=userId) & Q(enabled=1) & Q(deletemark=0)).values_list('roleid', flat=True))).values_list('targetid', flat=True)
        resourceIds = q1.union(q2)

        if targetCategory == 'piorganize':
            resourceIds,permissionScope = PermissionScopeService.TransformPermissionScope(userId, resourceIds)

        return resourceIds

    def TransformPermissionScope(self, userId, resourceIds):
        """
        转换用户的权限范围
        Args:
            userId (string): 用户主键
            resourceIds (string[]): 权限范围
        Returns:
        """
        permissionScope = PermissionScope.PermissionScopeDic.get('No')
        if resourceIds.count() > 0:
            userEntity = Piuser.objects.get(userid=userId)
            for r in resourceIds:
                if r == PermissionScope.PermissionScopeDic.get('All'):
                    permissionScope = PermissionScope.PermissionScopeDic.get('All')
                    continue
                if r == PermissionScope.PermissionScopeDic.get('UserCompany'):
                    permissionScope = PermissionScope.PermissionScopeDic.get('UserCompany')
                    continue
                if r == PermissionScope.PermissionScopeDic.get('UserDepartment'):
                    permissionScope = PermissionScope.PermissionScopeDic.get('UserDepartment')
                    continue
                if r == PermissionScope.PermissionScopeDic.get('UserWorkgroup'):
                    permissionScope = PermissionScope.PermissionScopeDic.get('UserWorkgroup')
                    continue
            return resourceIds,permissionScope
        return resourceIds, permissionScope


    def GetOrganizeIdsSql(self, managerUserId, permissionItemCode):
        """
        获得用户的权限范围设置
        Args:
            managerUserId (string): 用户主键
            permissionItemCode (string[]): 权限范围编号
        Returns:
            returnValue (Pipermissionscope): 用户的权限范围
        """

    def GetUserPermissionScope(self, managerUserId, permissionItemCode):
        """
        获得用户的权限范围设置
        Args:
            managerUserId (string): 用户主键
            permissionItemCode (string[]): 权限范围编号
        Returns:
            returnValue (Pipermissionscope): 用户的权限范围
        """
        permissionItemId = Pipermissionitem.objects.get(code=permissionItemCode).id
        organizeIds = Pipermissionscope.objects.filter(Q(targetcategory='PIORGANIZE') & Q(deletemark=0) & Q(enabled=1) & Q(targetid__isnull=False) & Q(permissionid=permissionItemId) & (
            (Q(resourcecategory='PIUSER') & Q(resourceid=managerUserId)) | (Q(resourcecategory='PIROLE') & Q(resourceid__in=Piuserrole.objects.filter(Q(userid=managerUserId) & Q(deletemark=0) & Q(enabled=1)).values_list('roleid', flat=True)))
        )).values_list('targetid', flat=True)

        returnValue = PermissionScope.PermissionScopeDic.get('No')
        for permissionScope in PermissionScope.PermissionScopeDic:
            if permissionScope in organizeIds:
                returnValue = permissionScope
        return returnValue



