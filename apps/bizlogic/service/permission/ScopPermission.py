# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2018/12/12 8:48'

from apps.bizlogic.service.base.UserRoleService import UserRoleService
from apps.bizlogic.service.base.PermissionScopeService import PermissionScopeService

from apps.bizlogic.models import Piuser
from apps.bizlogic.models import Pipermissionitem
from apps.bizlogic.models import Pipermissionscope
from apps.bizlogic.models import Piuserrole
from apps.bizlogic.models import Pirole

from apps.utilities.publiclibrary.SystemInfo import SystemInfo
from apps.utilities.publiclibrary.DbCommonLibaray import DbCommonLibaray
from apps.utilities.publiclibrary.StringHelper import StringHelper

from django.db.models import Q

class ScopPermission(object):

    def GetUserDTByPermissionScope(self, userId, permissionItemCode):
        """
          按某个权限范围获取特定用户可访问的用户列表
          Args:
              userId (string): 用户主键
              permissionItemCode (string): 操作权限编号
          Returns:
              returnValue(Piuser[]): 用户列表
        """
        isRole = False
        isRole = UserRoleService.UserInRole(self, userId, 'UserAdmin') | UserRoleService.UserInRole(self, userId, 'Admin')
        if(isRole):
            returnValue = Piuser.objects.filter(Q(isvisible=1) & Q(deletemark=0) & Q(enabled=1))
            return returnValue

        userids = ScopPermission.GetUserIdsSql(self, userId, permissionItemCode)
        returnValue = Piuser.objects.filter(Q(isvisible=1) & Q(enabled=1) & Q(id__in=userids)).order_by('sortcode')
        return returnValue

    def GetUserIdsByPermissionScope(self, userId, permissionItemCode):
        pass

    def GetRoleDTByPermissionScope(self, userId, permissionItemCode):
        pass

    def GetRoleIdsByPermissionScope(self, userId, permissionItemCode):
        pass

    def GetModuleDTByPermissionScope(self, userId, permissionItemCode):
        pass

    def GetPermissionItemDTByPermissionScope(self, userId, permissionItemCode):
        pass

    def GetOrganizeDTByPermissionScope(self, userId, permissionItemCode):
        pass

    def GetOrganizeIdsByPermissionScope(self, userId, permissionItemCode):
        pass

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
        organizeIds = ScopPermission.GetOrganizeIds(self, managerUserId,permissionItemCode)
        if organizeIds.count() > 0:
            sqlQuery2 = Piuser.objects.filter(Q(deletemark=0) & (Q(companyid__in=organizeIds) | Q(departmentid__in=organizeIds) | Q(workgroupid__in=organizeIds)) ).values_list('id', flat=True)
            sqlQuery = sqlQuery.union(sqlQuery2)

        #被管理部门的列表
        roleIds = ScopPermission.GetRoleIds(self, managerUserId, permissionItemCode)
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
        ids = ScopPermission.GetTreeResourceScopeIds(self, managerUserId, 'PIORGANIZE', permissionItemCode, False)

        #这里列出只是有效地，没被删除的组织机构主键
        if ids:
            ids = Pirole.objects.filter(Q(id__in=ids) & Q(enabled=1) & Q(deletemark=0)).values_list('id', flat=True)
        return ids


    def GetTreeResourceScopeIds(self, userId, tableName, permissionItemCode, childrens):
        """
          树型资源的权限范围
          Args:
              userId (string): 用户主键
              tableName (string): 资源分类
              permissionItemCode (string): 权限编号
              childrens (string): 是否含子节点
          Returns:
              returnValue(string[]): 主键列表
        """
        resourceScopeIds = ScopPermission.GetResourceScopeIds(self, userId, tableName, permissionItemCode)

        if not childrens:
            return resourceScopeIds

        idList = StringHelper.ArrayToList(self, resourceScopeIds, ',')
        if idList:
            sqlQuery = 'select id from ( select id from ' + tableName + ' where (id in (' + idList + ')) UNION ALL select ResourceTree.Id AS ID FROM ' + tableName + ' AS ResourceTree INNER JOIN pipermissionscope AS A ON A.Id = ResourceTree.ParentId) AS PermissionScopeTree'
            dataTable = DbCommonLibaray.executeQuery(self, sqlQuery)
            #TODO:这个地方需要把两个列表合并
            #resourceScopeIds + dataTable
        return resourceScopeIds

    def GetResourceScopeIds(self, userId, targetCategory, permissionItemCode):
        """
          获得用户的某个权限范围资源主键数组
          Args:
              userId (string): 用户主键
              targetCategory (string): 资源分类
              permissionItemCode (string): 权限编号
              childrens
          Returns:
              returnValue(string[]): 主键列表
        """
        permissionItemId = Pipermissionitem.objects.get(code=permissionItemCode).id
        defaultRoleId = Piuser.objects.get(id = userId).roleid

        q1 = Pipermissionscope.objects.filter(Q(resourcecategory='PIUSER') & Q(resourceid=userId) & Q(targetcategory=permissionItemId) & Q(enabled=1) & Q(deletemark=0)).values_list('targetid', flat=True)
        if defaultRoleId:
            q2 = Pipermissionscope.objects.filter(Q(resourcecategory='PIROLE') & Q(targetcategory=targetCategory) & Q(permissionid=permissionItemId) & Q(deletemark=0) & Q(enabled=1) & Q(resourceid__in=Piuserrole.objects.filter(Q(userid=userId) & Q(enabled=1) & Q(deletemark=0)).values_list('roleid', flat=True))).values_list('roleid', flat=True)
        else:
            q2 = Pipermissionscope.objects.filter(Q(resourcecategory='PIROLE') & Q(targetcategory=targetCategory) & Q(permissionid=permissionItemId) & Q(deletemark=0) & Q(enabled=1) & (Q(resourceid__in=Piuserrole.objects.filter(Q(userid=userId) & Q(enabled=1) & Q(deletemark=0)).values_list('roleid', flat=True)) | Q(resourceid=defaultRoleId))).values_list('targetid', flat=True)

        resourceIds = q1.union(q2)

        if SystemInfo.EnableOrganizePermission:
            userEntity = Piuser.objects.get(id=userId)
            q3 = Pipermissionscope.objects.filter(Q(resourcecategory='PIORGANIZE') & (Q(resourceid=userEntity.companyid) | Q(resourceid=userEntity.departmentid) | Q(resourceid=userEntity.workgroupid)) & Q(targetcategory=targetCategory) & Q(permissionid=permissionItemId) & Q(enabled=1) & Q(deletemark=0)).values_list('targetid', flat=True)
            resourceIds.union(q3)

        if targetCategory == 'PIORGANIZE':
            resourceIds, permissionScope = PermissionScopeService.TransformPermissionScope(self, userId, resourceIds)


        return resourceIds

    def GetRoleIds(self, managerUserId, permissionItemCode):
        #这是一个QuerySet
        roleIds = ScopPermission.GetRoleIdsSql(self, managerUserId, permissionItemCode)
        if roleIds.count() > 0:
            return Pirole.objects.filter(Q(id__in=roleIds) & Q(enabled=1) & Q(deletemark=0)).values_list('id', flat=True)
        return roleIds


    def GetRoleIdsSql(self, managerUserId, permissionItemCode):
        permissionItemId = Pipermissionitem.objects.get(code=permissionItemCode).id
        '''
        sqlQuery += " SELECT PIPERMISSIONSCOPE.TARGETID AS " + BusinessLogic.FieldId
                      + "   FROM PIPERMISSIONSCOPE "
                      + "  WHERE (PIPERMISSIONSCOPE.TARGETID IS NOT NULL "
                      + "        AND PIPERMISSIONSCOPE.TARGETCATEGORY = '" + PiRoleTable.TableName + "' "
                      + "        AND ((PIPERMISSIONSCOPE.RESOURCECATEGORY = '" + PiUserTable.TableName + "' "
                      + "             AND PIPERMISSIONSCOPE.RESOURCEID = '" + managerUserId + "')"
                      // 以及 他所在的角色在管理的角色
                      + "        OR (PIPERMISSIONSCOPE.RESOURCECATEGORY = '" + PiRoleTable.TableName + "'"
                      + "            AND PIPERMISSIONSCOPE.RESOURCEID IN ( " 
                      +                             " SELECT ROLEID " 
                      +                             "   FROM " + PiUserRoleTable.TableName
                      + "  WHERE (" + PiUserRoleTable.FieldUserId + " = '" + managerUserId + "' "
                      + "        AND " + PiUserRoleTable.FieldEnabled + " = 1))))" 
                      // 并且是指定的本权限
                      + "        AND " + PiPermissionScopeTable.FieldPermissionId + " = '" + permissionItemId + "')";
        '''
        q1 =    Pipermissionscope.objects.filter(Q(targetid__isnull=False) & Q(targetcategory='PIROLE') & ((Q(resourcecategory='PIUSER') & Q(resourceid=managerUserId))|(Q(resourcecategory='PIROLE') & Q(resourceid__in=Piuserrole.objects.filter(Q(userid=managerUserId) & Q(enabled=1)).values_list('roleid', flat=True)))) & Q(permissionid=permissionItemId))

        organizeIds = ScopPermission.GetOrganizeIds(self, managerUserId, permissionItemCode)
        if organizeIds.count() > 0:
            q2 = Pirole.objects.filter(Q(enabled=1) & Q(deletemark=0) & Q(organizeid__in=organizeIds)).values_list('id', flat=True)
            return q1.union(q2)
        return q1