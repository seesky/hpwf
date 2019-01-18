# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2019/1/17 8:28'

from apps.bizlogic.models import Citablecolumns
from apps.bizlogic.models import Pitablepermissionscope
from apps.bizlogic.models import Pipermissionscope
from apps.bizlogic.service.base.PermissionScopeService import PermissionScopeService
from apps.bizlogic.service.base.PermissionItemService import PermissionItemService
from apps.bizlogic.service.base.UserRoleService import UserRoleService

from django.db.utils import DatabaseError
from django.db.transaction import TransactionManagementError
from django.db.models import Q

from apps.utilities.message.StatusCode import StatusCode
from apps.utilities.message.FrameworkMessage import FrameworkMessage
from apps.utilities.publiclibrary.DbCommonLibaray import DbCommonLibaray
from apps.utilities.publiclibrary.ConstrainUtil import ConstrainUtil

class TableColumnsService(object):

    def Add(entity):
        """
        新增数据
        Args:
            entity (Citablecolumns): 实体
        Returns:
        """
        try:
            entity.save()
            returnCode = StatusCode.statusCodeDic['OKAdd']
            returnMessage = FrameworkMessage.MSG0009
            returnValue = entity.id
            return returnCode, returnMessage, returnValue
        except DatabaseError as e:
            print(e)
            returnCode = StatusCode.statusCodeDic['DbError']
            returnMessage = FrameworkMessage.MSG0001
            returnValue = None
            return returnCode, returnMessage, returnValue
        except TransactionManagementError as e:
            print(e)
            returnCode = StatusCode.statusCodeDic['DbError']
            returnMessage = FrameworkMessage.MSG0001
            returnValue = None
            return returnCode, returnMessage, returnValue

    def GetDT(self):
        """
        取得列表
        Args:
        Returns:
            returnValue (Citablecolumns[]): 实体列表
        """
        returnValue = Citablecolumns.objects.filter(deletemark=0)
        return returnValue

    def GetAllTableScope(self):
        """
        得到所有数据表（用于表字段权限的控制，主要针对PiTablePermissionScope数据表的数据）
        Args:
        Returns:
            returnValue (Citablecolumns[]): 实体列表
        """
        returnValue = Pitablepermissionscope.objects.filter(deletemark=0)
        return returnValue

    def GetTableNameAndCode(self):
        """
        得到所有数据表（表的中文名称与英文名称）
        Args:
        Returns:
            returnValue (Citablecolumns[]): 实体列表
        """
        sqlQuery = "SELECT DISTINCT TABLECODE,TABLECODE AS TABLENAME FROM CITABLECOLUMNS ORDER BY TABLECODE"
        returnValue = DbCommonLibaray.executeQuery(None, sqlQuery)
        return returnValue

    def GetEntity(id):
        """
        取得实体
        Args:
            id (string): 主键
        Returns:
            returnValue (Citablecolumns or None): 实体
        """
        try:
            user = Citablecolumns.objects.get(id=id)
            return user
        except Citablecolumns.DoesNotExist:
            return None

    def Update(entity):
        """
        更新实体
        Args:
            userEntity (Citablecolumns): 实体
        Returns:
            returnValue (string): 状态码
            returnMessage (string): 状态信息
        """
        try:
            entity.save()
            returnCode = StatusCode.statusCodeDic['OKUpdate']
            returnMessage = FrameworkMessage.MSG0010
            return returnCode, returnMessage
        except:
            returnCode = StatusCode.statusCodeDic['Error']
            returnMessage = FrameworkMessage.MSG0001
            return returnCode, returnMessage

    def GetDTByIds(ids):
        """
        按主键数组获取数据列表
        Args:
            ids (string[]): 主键列表
        Returns:
            returnValue (Citablecolumns[]): 实体列表
        """
        returnValue = Citablecolumns.objects.filter(Q(id__in=ids) & Q(deletemark=0))

    def GetDTByValues(valuesDic):
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
        returnValue = Citablecolumns.objects.filter(q)
        return returnValue

    def BatchSave(dataTable):
        """
        批量保存数据
        Args:
            dataTable (Citablecolumns[]): 列表
        Returns:
            returnValue (True or False): 保存结果
        """
        try:
            for column in dataTable:
                column.save()
            return True
        except:
            return False

    def Delete(id):
        """
        刪除资料
        Args:
            id (string): 主键
        Returns:
            returnValue (int): 影响行数
        """
        returnValue = Citablecolumns.objects.filter(id = id).delete()
        return returnValue

    def BatchDelete(ids):
        """
        刪除资料
        Args:
            ids (string[]): 主键列表
        Returns:
            returnValue (int): 影响行数
        """
        returnValue = Citablecolumns.objects.filter(id__in=ids).delete()
        return returnValue

    def SetDeleted(ids):
        """
        批量设置删除标志
        Args:
            ids (string[]): 主键列表
        Returns:
            returnValue (int): 影响行数
        """
        returnValue = Citablecolumns.objects.filter(id__in=ids).update(deletemark = 1)
        return returnValue

    def GetSearchFields(tableCode):
        """
        得到查询项
        Args:
            tableCode (string): 表名称
        Returns:
            returnValue (): 数据表
        """
        sqlQuery = "SELECT " + 'columncode' + "," \
            + 'columnname' + "," \
            + 'datatype' \
            + " FROM " + 'citablecolumns' \
            + " WHERE " + 'tablecode' + "='" + tableCode + "' AND " \
            + 'issearchcolumn' + "= 1 AND " \
            + 'deletemark' + "= 0" \
            + " ORDER BY " + 'sortcode'
        returnValue = DbCommonLibaray.executeQuery(None, sqlQuery)
        return returnValue

    def GetColumns(userInfo, tableCode, permissionCode = "Column.Access"):
        """
        获取用户的列权限
        Args:
            tableCode (string): 表名称
            permissionCode (string): 操作权限
        Returns:
            returnValue (): 数据表
        """
        if permissionCode == "Column.Deney" or permissionCode == "Column.Edit":
            #按数据权限来过滤数据
            returnValue = PermissionScopeService.GetResourceScopeIds(None, userInfo.Id, tableCode, permissionCode)
        elif permissionCode == "Column.Access":
            #1: 用户有权限的列名
            returnValue = PermissionScopeService.GetResourceScopeIds(None, userInfo.Id, tableCode, permissionCode)
            #2: 先获取公开的列名
            publicIds = Citablecolumns.objects.filter(Q(tablecode=tableCode) & Q(ispublic=1)).values_list('columncode', flat=True)
            returnValue = returnValue.union(publicIds)
            return returnValue

    def GetDTByTable(tableCode):
        """
        按表名获取字段列表
        Args:
            tableCode (string): 表名称
        Returns:
            returnValue (): 数据表
        """
        returnValue = Citablecolumns.objects.filter(Q(tablecode=tableCode) & Q(deletemark=0))
        return returnValue

    def GetTablePermissionScope(self):
        """
        得到所有可做表字段控制权限的数据
        Args:
        Returns:
            returnValue (): 数据表
        """
        returnValue = Pitablepermissionscope.objects.filter(Q(deletemark=0))
        return returnValue

    def GetConstraintDT(resourceCategory, resourceId, permissionCode = "Resource.AccessPermission"):
        """
        获取约束条件（所有的约束）
        Args:
            resourceCategory (string): 资源类别
            resourceId (string): 资源主键
        Returns:
            returnValue (): 数据表
        """
        permissionId = ''
        permissionId = PermissionItemService.GetIdByAdd(permissionCode)

        sqlQuery = " SELECT PIPERMISSIONSCOPE.ID  , PITABLEPERMISSIONSCOPE.ITEMVALUE TABLECODE, PITABLEPERMISSIONSCOPE.ITEMNAME TABLENAME, PIPERMISSIONSCOPE.PERMISSIONCONSTRAINT, PITABLEPERMISSIONSCOPE.SORTCODE FROM(" + \
                "SELECT ITEMVALUE, ITEMNAME, SORTCODE FROM PITABLEPERMISSIONSCOPE WHERE(DELETEMARK=0) AND(ENABLED=1) )  PITABLEPERMISSIONSCOPE LEFT OUTER JOIN (SELECT ID, TARGETID, PERMISSIONCONSTRAINT FROM PIPERMISSIONSCOPE WHERE (RESOURCECATEGORY = '" + resourceCategory + "') AND(RESOURCEID='" + resourceId + "') AND(TARGETCATEGORY='Table') AND(PERMISSIONID='" + permissionId + "') AND(DELETEMARK=0) AND(ENABLED=1) )  PIPERMISSIONSCOPE" + \
                "ON PITABLEPERMISSIONSCOPE.ITEMVALUE = PIPERMISSIONSCOPE.TARGETID ORDER BY PITABLEPERMISSIONSCOPE.SORTCODE"
        dataTable = DbCommonLibaray.executeQuery(None, sqlQuery)
        return dataTable

    def GetUserConstraint(userInfo, tableName, permissionCode = "Resource.AccessPermission"):
        """
        获取约束条件（所有的约束）
        Args:
            tableName (string): 表名
            permissionCode (string): 权限代码
        Returns:
            returnValue (): 数据表
        """
        returnValue = ''
        permissionId = ''
        permissionId = PermissionItemService.GetIdByAdd(permissionCode)
        roleIds = UserRoleService.GetAllRoleIds(None, userInfo.Id)
        if not roleIds or len(roleIds) == 0:
            return returnValue

        dtPermissionScope = Pipermissionscope.objects.filter(Q(resourcecategory='pirole') & Q(resourceid__in=roleIds) & Q(targetcategory='Table') & Q(targetid=tableName) & Q(permissionid=permissionId) & Q(enabled=1) & Q(deletemark=0))
        permissionConstraint = ''
        for dataRow in dtPermissionScope:
            permissionConstraint = dataRow.permissionconstraint
            permissionConstraint = str(permissionConstraint).strip()
            if permissionConstraint:
                returnValue = returnValue + " AND " + permissionConstraint
        #得到当前用户的约束条件
        userConstraint = TableColumnsService.GetConstraint('piuser', userInfo.Id, tableName)
        if not userConstraint:
            userConstraint = ''
        else:
            returnValue = returnValue + " AND " + userConstraint

        if returnValue:
            returnValue = str(returnValue)[5:]
            returnValue = ConstrainUtil.PrepareParameter(userInfo, returnValue)

        return returnValue

    def SetConstraint(resourceCategory, resourceId, tableName, permissionCode, constraint, enabled = True):
        returnValue = PermissionScopeService.GetIdByAdd(resourceCategory, resourceId, tableName, permissionCode, constraint, enabled)
        return returnValue

    def GetConstraint(resourceCategory, resourceId, tableName, permissionCode = "Resource.AccessPermission"):
        entity = TableColumnsService.GetConstraintEntity(resourceCategory, resourceId, tableName, permissionCode)
        if entity and entity.enabled == 1:
            returnValue = entity.permissionconstraint
        return returnValue

    def GetConstraintEntity(resourceCategory, resourceId, tableName, permissionCode = "Resource.AccessPermission"):
            entity = None
            permissionId = ''
            permissionId = PermissionItemService.GetIdByAdd(permissionCode)

            dt = Pipermissionscope.objects.filter(Q(resourcecategory=resourceCategory) & Q(resourceid=resourceId) & Q(targetcategory='Table') & Q(targetid=tableName) & Q(permissionid=permissionId) & Q(deletemark=0))
            return dt

    def BatchDeleteConstraint(ids):
        """
        批量删除约束条件
        Args:
            ids (string[]): 主键列表
        Returns:
            returnValue (): 数据表
        """
        returnValue = Pipermissionscope.objects.filter(id__in=ids)
        return returnValue

    def AddTablePermissionScope(entity):
        """
        增加可做表权限控制的数据表
        Args:
            entity (Pitablepermissionscope): 实体
        Returns:
            returnValue (): 数据表
        """
        try:
            entity.save()
            returnCode = StatusCode.statusCodeDic['OKAdd']
            returnMessage = FrameworkMessage.MSG0009
            returnValue = entity.id
            return returnCode, returnMessage, returnValue
        except DatabaseError as e:
            print(e)
            returnCode = StatusCode.statusCodeDic['DbError']
            returnMessage = FrameworkMessage.MSG0001
            returnValue = None
            return returnCode, returnMessage, returnValue
        except TransactionManagementError as e:
            print(e)
            returnCode = StatusCode.statusCodeDic['DbError']
            returnMessage = FrameworkMessage.MSG0001
            returnValue = None
            return returnCode, returnMessage, returnValue

    def DeleteTablePermissionScope(valuesDic):
        """
        按键值对删除
        valueDic = {key:value, key:value, ...}
        Args:
            valueDic (Dic{key:value}): 参数和值对
        Returns:
            returnValue (int): 影响行数
        """
        q = Q()
        for i in valuesDic:
            q.add(Q(**{i: valuesDic[i]}), Q.AND)
        returnValue = Pitablepermissionscope.objects.filter(q).delete()
        return returnValue

    def SetTablePermissionScopeDeleted(ids):
        """
        按主键列表删除
        Args:
            ids (string[]): 主键列表
        Returns:
            returnValue (int): 影响行数
        """
        returnValue = Pitablepermissionscope.objects.filter(id__in=ids).update(deletemark=1)
        return returnValue

    def GetTablePermissionScopeEntity(name, value):
        """
        取得表权限控制数据表实体
        Args:
            name (string): 字段名称
            value (string): 字段值
        Returns:
            returnValue (Pitablepermissionscope): 实体
        """
        q = Q()
        q.add({name:value})
        scope = Pitablepermissionscope.objects.filter(q)
        return scope