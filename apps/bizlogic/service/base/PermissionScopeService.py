# _*_ coding: utf-8 _*_
__author__ = 'baxuelong@163.com'
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
from apps.utilities.publiclibrary.SystemInfo import SystemInfo
from apps.bizlogic.service.base.PermissionItemService import PermissionItemService

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

        if targetCategory == 'PIORGANIZE':
            resourceIds,permissionScope = PermissionScopeService.TransformPermissionScope(None, userId, resourceIds)

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
        if len(resourceIds) > 0:
            userEntity = Piuser.objects.get(id=userId)
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

        if ids and len(ids) > 0:
            return  Piorganize.objects.filter(Q(id__in=ids) & Q(enabled=1) & Q(deletemark=0))
        else:
            return None

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

        if ids and len(ids) > 0:
            userEntity = Piuser.objects.get(id=managerUserId)
            for i in range(ids.count()):
                if ids[i] == PermissionScope.PermissionScopeDic.get('User'):
                    ids[i] = userEntity.id
                    break
        if ids and len(ids) > 0:
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
        sqlQuery = Pipermissionscope.objects.filter(Q(targetcategory='PIUSER') & Q(resourceid=managerUserId) & Q(resourcecategory='PIUSER') & Q(permissionid=permissionItemId) & Q(targetid__isnull=False)).values_list('targetid', flat=True)
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

        q1 = Pipermissionscope.objects.filter(Q(resourcecategory='PIUSER') & Q(resourceid=userId) & Q(targetcategory=targetCategory) & Q(enabled=1) & Q(deletemark=0)).values_list('targetid', flat=True)
        if defaultRoleId:
            q2 = Pipermissionscope.objects.filter(Q(resourcecategory='PIROLE') & Q(targetcategory=targetCategory) & Q(permissionid=permissionItemId) & Q(deletemark=0) & Q(enabled=1) & Q(resourceid__in=Piuserrole.objects.filter(Q(userid=userId) & Q(enabled=1) & Q(deletemark=0)).values_list('roleid', flat=True))).values_list('targetid', flat=True)
        else:
            q2 = Pipermissionscope.objects.filter(Q(resourcecategory='PIROLE') & Q(targetcategory=targetCategory) & Q(permissionid=permissionItemId) & Q(deletemark=0) & Q(enabled=1) & (Q(resourceid__in=Piuserrole.objects.filter(Q(userid=userId) & Q(enabled=1) & Q(deletemark=0)).values_list('roleid', flat=True)) | Q(resourceid=defaultRoleId))).values_list('targetid', flat=True)

        resourceIds = q1.union(q2)

        if SystemInfo.EnableOrganizePermission:
            userEntity = Piuser.objects.get(id=userId)
            q3 = Pipermissionscope.objects.filter(Q(resourcecategory='PIORGANIZE') & (Q(resourceid=userEntity.companyid) | Q(resourceid=userEntity.departmentid) | Q(resourceid=userEntity.workgroupid)) & Q(targetcategory=targetCategory) & Q(permissionid=permissionItemId) & Q(enabled=1) & Q(deletemark=0)).values_list('targetid', flat=True)
            resourceIds = resourceIds.union(q3)

        if targetCategory == 'PIORGANIZE':
            resourceIds, permissionScope = PermissionScopeService.TransformPermissionScope(self, userId, resourceIds)


        return resourceIds

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
        resourceScopeIds = PermissionScopeService.GetResourceScopeIds(self, userId, tableName, permissionItemCode)

        if not childrens:
            return resourceScopeIds

        idList = StringHelper.ObjectsToList(resourceScopeIds)
        if idList:
            sqlQuery = 'select id from ( select id from ' + tableName + ' where (id in (' + idList + ')) UNION ALL select ResourceTree.Id AS ID FROM ' + tableName + ' AS ResourceTree INNER JOIN pipermissionscope AS A ON A.Id = ResourceTree.ParentId) AS PermissionScopeTree'
            dataTable = DbCommonLibaray.executeQuery(self, sqlQuery)
            #TODO:这个地方需要把两个列表合并
            #resourceScopeIds + dataTable
        return resourceScopeIds

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

        organizeIds = PermissionScopeService.GetOrganizeIds(self, managerUserId, permissionItemCode)
        if organizeIds.count() > 0:
            q2 = Pirole.objects.filter(Q(enabled=1) & Q(deletemark=0) & Q(organizeid__in=organizeIds)).values_list('id', flat=True)
            return q1.union(q2)
        return q1

    def GetRoleIds(self, managerUserId, permissionItemCode):
        #这是一个QuerySet
        roleIds = PermissionScopeService.GetRoleIdsSql(self, managerUserId, permissionItemCode)
        if roleIds.count() > 0:
            return Pirole.objects.filter(Q(id__in=roleIds) & Q(enabled=1) & Q(deletemark=0)).values_list('id', flat=True)
        return roleIds

    def GetDT(valuesDic):
        """
        按键值对获取列表
        valueDic = {key:value, key:value, ...}
        Args:
            valueDic (Dic{key:value}): 参数和值对
        Returns:
            returnValue (Pioranize[]): 角色列表
        """
        q = Q()
        for i in valuesDic:
            q.add(Q(**{i: valuesDic[i]}), Q.AND)
        returnValue = Pipermissionitem.objects.filter(q)
        return returnValue

    def GetIdByAdd(resourceCategory, resourceId, tableName, permissionCode, constraint, enabled = True):
        permissionId = PermissionItemService.GetIdByAdd(permissionCode)

        # Pipermissionitem.objects.get_or_create(defaults={'deletemark': '0', 'enabled': '1', 'code': permissionCode},
        #                                        code=permissionCode,
        #                                        fullname=permissionCode if None else None,
        #                                        categorycode="Application",
        #                                        parentid=None,
        #                                        isscope=0,
        #                                        ispublic=0,
        #                                        allowdelete=1,
        #                                        allowedit=1,
        #                                        enabled=1,
        #                                        deletemark=0,
        #                                        moduleid=None
        #                                        )

        Pipermissionitem.objects.get_or_create(deletemark = 0, enabled = 1, code = permissionCode, defaults={'code':permissionCode,'fullname':(permissionCode if None else None),'categorycode':"Application",'parentid':None,'isscope':0,'ispublic':0, 'allowdelete':1,'allowedit':1, 'enabled':1, 'deletemark':0, 'moduleid':None})

        permissionId = Pipermissionitem.objects.get(Q(code=permissionCode) & Q(deletemark=0) & Q(enabled=1))


        Pipermissionscope.objects.get_or_create(
            defaults={'resourcecategory': resourceCategory, 'resourceid': resourceId, 'targetcategory': 'Table',
                      'targetid': tableName, 'deletemark': 0},
            resourcecategory=resourceCategory,
            resourceid=resourceId,
            targetcategory='Table',
            targetid=tableName,
            permissionconstraint=constraint,
            permissionid=permissionId,
            deletemark=0,
            enabled=1 if enabled else 0
            )

        Pipermissionscope.objects.get_or_create(resourcecategory= resourceCategory, resourceid=resourceId, targetcategory='Table',targetid=tableName, deletemark=0,
            defaults={'resourcecategory':resourceCategory, 'resourceid':resourceId,'targetcategory':'Table','targetid':tableName,'permissionconstraint':constraint,'permissionid':permissionId,'deletemark':0,'enabled':(1 if enabled else 0)}
        )

        scope = Pipermissionscope.objects.get(
            Q(resourcecategory=resourceCategory) & Q(resourceid=resourceId) & Q(targetcategory='Table') & Q(
                targetid=tableName) & Q(permissionconstraint=constraint) & Q(permissionid=permissionId) & Q(
                deletemark=0))

        scope.permissionconstraint = 1 if enabled else 0
        scope.enabled = 1 if enabled else 0
        scope.save()
        return scope.id






