# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2018/12/19 16:02'

from apps.bizlogic.models import Pipermissionitem
from apps.bizlogic.models import Pipermissionscope
from apps.bizlogic.models import Piuser
from apps.bizlogic.models import Piuserrole
from apps.bizlogic.models import Piorganize
from apps.bizlogic.models import Pirole

from apps.utilities.message.PermissionScope import PermissionScope
from apps.utilities.publiclibrary.StringHelper import StringHelper
from apps.utilities.publiclibrary.DbCommonLibaray import DbCommonLibaray

#from apps.bizlogic.service.permission.ScopPermission import ScopPermission

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

    def GetOrganizeDT(self, managerUserId, permissionItemCode):
        """
        按某个权限获取组织机构数据表
        Args:
            managerUserId (string): 用户主键
            permissionItemCode (string[]): 权限范围编号
        Returns:
            returnValue (Pipermissionscope): 用户的权限范围
        """
        ids = PermissionScopeService.GetTreeResourceScopeIds(self, managerUserId, 'PIORGANIZE', permissionItemCode, False)

        if ids & ids.count() > 0:
            return  Piorganize.objects.filter(Q(id__in=ids) & Q(enabled=1) & Q(deletemark=0))

    def GetOrganizeIds(self, managerUserId, permissionItemCode):
        """
        按某个权限获取组织机构数据表
        Args:
            managerUserId (string): 用户主键
            permissionItemCode (string[]): 权限范围编号
        Returns:
            returnValue (string[]): 主键数组
        """
        ids = PermissionScopeService.GetTreeResourceScopeIds(self, managerUserId, 'PIORGANIZE', permissionItemCode, False)
        if ids & ids.count > 0:
            ids = Piorganize.objects.filter(Q(id__in=ids) & Q(enabled=1) & Q(deletemark=0)).values_list('id', flat=True)
        return ids

    def GetUserIds(self, managerUserId, permissionItemCode):
        """
        按某个权限获取员工 主键数组
        Args:
            managerUserId (string): 用户主键
            permissionItemCode (string[]): 权限范围编号
        Returns:
            returnValue (string[]): 主键数组
        """
        ids = PermissionScopeService.GetTreeResourceScopeIds(self, managerUserId, 'PIORGANIZE', permissionItemCode, True)
        if PermissionScope.PermissionScopeDic.get('User') in ids:
            return [managerUserId]

        dataTable = PermissionScopeService.GetUserIdsSql(self, managerUserId, permissionItemCode)

        if ids & ids.count() > 0:
            userEntity = Piuser.objects.get(id=managerUserId)
            for i in range(ids.count()):
                if ids[i] == PermissionScope.PermissionScopeDic.get('User'):
                    ids[i] = userEntity.id
                    break
        if ids & ids.count():
            ids = Piuser.objects.filter(Q(id__in=ids) & Q(enabled=1) & Q(deletemark=0)).values_list('id', flat=True)
        return ids

    def GetUserIdsSql(self, managerUserId, permissionItemCode):
        """
          按某个权限获取员工
          Args:
              managerUserId (string): 管理用户主键
              permissionItemCode (string): 权限编号
          Returns:
              returnValue(Piuser[]): 用户列表
        """
        permissionItemId = Pipermissionitem.objects.get(code=permissionItemCode).id

        #直接管理的用户
        sqlQuery = Pipermissionscope.objects.filter(Q(targetcategory='PIUSER') & Q(resourceid=managerUserId) & Q(resourcecategory='PIUSER') & Q(permissionid=permissionItemCode) & Q(targetid__isnull=False)).values_list('targetid', flat=True)
        #被管理部门的列表
        organizeIds = PermissionScopeService.GetOrganizeIds(self, managerUserId,permissionItemCode)
        if organizeIds.count() > 0:
            sqlQuery2 = Piuser.objects.filter(Q(deletemark=0) & (Q(companyid__in=organizeIds) | Q(departmentid__in=organizeIds) | Q(workgroupid__in=organizeIds)) ).values_list('id', flat=True)
            sqlQuery = sqlQuery.union(sqlQuery2)

        #被管理部门的列表
        roleIds = PermissionScopeService.GetRoleIds(self, managerUserId, permissionItemCode)
        if roleIds.count() > 0:
            sqlQuery3 = Piuserrole.objects.filter(Q(enabled=1) & Q(deletemark=0) & Q(roleid__in=roleIds)).values_list('userid', flat=True)
            sqlQuery = sqlQuery.union(sqlQuery3)

        return sqlQuery

    def GetOrganizeIds(self, managerUserId, permissionItemCode):
        """
          按某个权限获取组织机构 主键数组
          Args:
              managerUserId (string): 管理用户主键
              permissionItemCode (string): 权限编号
          Returns:
              returnValue(Piuser[]): 用户列表
        """
        #这里应该考虑，当前用户的管理权限是，所在公司？所在部门？所以在工作组等情况
        ids = PermissionScopeService.GetTreeResourceScopeIds(self, managerUserId, 'PIORGANIZE', permissionItemCode, False)

        #这里列出只是有效地，没被删除的组织机构主键
        if ids:
            ids = Pirole.objects.filter(Q(id__in=ids) & Q(enabled=1) & Q(deletemark=0)).values_list('id', flat=True)
        return ids

    def GetRoleIds(self, managerUserId, permissionItemCode):
        #这是一个QuerySet
        roleIds = PermissionScopeService.GetRoleIdsSql(self, managerUserId, permissionItemCode)
        if roleIds.count() > 0:
            return Pirole.objects.filter(Q(id__in=roleIds) & Q(enabled=1) & Q(deletemark=0)).values_list('id', flat=True)
        return roleIds







