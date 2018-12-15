# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2018/12/11 15:01'

from apps.bizlogic.models import Piuser
from apps.bizlogic.models import Piuserrole
from apps.bizlogic.models import Pistaff

from django.db.utils import DatabaseError
from django.db.transaction import TransactionManagementError
from django.db import connection
from django.core.paginator import Paginator
from django.db.models import Q

from utilities.publiclibrary.StringHelper import StringHelper
from utilities.message.StatusCode import StatusCode
from utilities.message.FrameworkMessage import FrameworkMessage
from utilities.message.AuditStatus import AuditStatus
from utilities.publiclibrary.DbCommonLibaray import DbCommonLibaray

from apps.bizlogic.service.base.OrganizeService import OrganizeService
from apps.bizlogic.service.permission.UserPermission import UserPermission

class UserSerivce(object):
    """
    用户服务
    """

    def __init__(self):
        object.__init__()

    def Exists(self, fieldNames, fieldValue):
        """
        用户名是否重复
        Args:
            fieldNames (string): 字段名
            fieldValue (string): 字段值
        Returns:
            returnValue(bool): 已存在
        """
        try:
            Piuser.objects.get(**{fieldNames: fieldValue})
            return True
        except Piuser.DoesNotExist:
            return False

    def AddUser(self, userEntity):
        """
        添加用户
        Args:
            userEntity (Piuser): 用户实体
        Returns:
            returnValue: 用户主键
        """
        try:
            userEntity.save()
            returnCode = StatusCode.statusCodeDic['OKAdd']
            returnMessage = FrameworkMessage.MSG0009
            returnValue = userEntity.id
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

    def GetEntity(id):
        """
        获取用户实体
        Args:
            id (string): 用户主键
        Returns:
            returnValue (Piuser or None): 用户实体
        """
        try:
            user = Piuser.objects.get(id=id)
            return user
        except Piuser.DoesNotExist:
            return None


    def GetEntityByUserName(self, userName):
        """
        根据用户名获取用户实体
        Args:
            userName (string): 用户名称
        Returns:
            returnValue (Piuser or None): 用户实体
        """
        try:
            user = Piuser.objects.get(username=userName)
            return user
        except Piuser.DoesNotExist:
            return None


    def GetDT(self):
        """
        获取用户列表
        Args:
        Returns:
            returnValue (List): 用户列表
        """
        returnValue = []
        try:
            for user in Piuser.objects.all():
                returnValue.append(user)
            return returnValue
        except DatabaseError as e:
            return returnValue
        except TransactionManagementError as e:
            return returnValue


    def GetDTByPage(self, searchValue, departmentId, roleId, pageSize=50, order=None):
        """
        分页查询
        Args:
            searchValue (string): 查询字段
            departmentId (string): 部门主键
            roleId (string): 角色主键
            pageSize (int): 每页显示
            order (string): 排序
        Returns:
            returnValue (List): 用户分页列表
        """
        countSqlQuery =' SELECT * FROM ' +  Piuser._meta.db_table + ' WHERE '

        whereConditional = Piuser._meta.db_table + '.DELETEMARK' + ' = 0 ' \
            + " AND " + Piuser._meta.db_table + '.ENABLED' + ' = 1 ' \
            + " AND " + Piuser._meta.db_table + '.ISVISIBLE' + ' = 1 '

        if departmentId:
            organizeIds = OrganizeService.GetChildrensById(self, departmentId)
            if len(organizeIds) != 0:
                whereConditional = whereConditional + " AND (" +  Piuser._meta.db_table + '.COMPANYID IN (' + StringHelper.ArrayToList(self,organizeIds,"\'") + ')' \
                    + " OR " + Piuser._meta.db_table + '.SUBCOMPANYID IN (' + StringHelper.ArrayToList(self,organizeIds,"\'") + ')' \
                    + " OR " + Piuser._meta.db_table + '.DEPARTMENTID IN (' + StringHelper.ArrayToList(self,organizeIds,"\'") + ')' \
                    + " OR " + Piuser._meta.db_table + '.SUBDEPARTMENTID IN (' + StringHelper.ArrayToList(self,organizeIds,"\'") + ')' \
                    + " OR " + Piuser._meta.db_table + '.WORKGROUPID IN (' + StringHelper.ArrayToList(self,organizeIds,"\'") + '))'

        if roleId:
            whereConditional = whereConditional + ' AND ( ' + Piuser._meta.db_table + '.ID IN' \
                + '    (SELECT USERID FROM ' + Piuserrole._meta.db_table \
                + '     WHERE ROLEID = \'' + roleId + '\'' \
                + '     AND ENABLED = 1' \
                + '     AND DELETEMARK = 0 ))'

        if searchValue:
            whereConditional = whereConditional + "  AND (" + searchValue + ')'

        countSqlQuery = countSqlQuery + ' ' + whereConditional
        userList = DbCommonLibaray.executeQuery(self, countSqlQuery)
        returnValue = Paginator(userList, pageSize)
        return returnValue

    def GetList(self):
        """
        获取用户列表
        Args:
        Returns:
            returnValue (List): 用户列表
        """
        returnValue = []
        try:
            for user in Piuser.objects.all():
                returnValue.append(user)
            return returnValue
        except DatabaseError as e:
            return returnValue
        except TransactionManagementError as e:
            return returnValue


    def GetDTByIds(self, ids):
        """
         按主键获取用户列表
        Args:
            ids (List[string]): 主键数组
        Returns:
            returnValue (List): 用户列表
        """
        returnValue = []
        for id in ids:
            try:
                user = Piuser.objects.get(id=id)
                returnValue.append(user)
            except Piuser.DoesNotExist:
                continue
        return returnValue

    def GetListByIds(self, ids):
        """
        按主键获取用户列表
        Args:
            ids (List[string]): 主键数组
        Returns:
            returnValue (List): 用户列表
        """
        returnValue = []
        for id in ids:
            try:
                user = Piuser.objects.get(id=id)
                returnValue.append(user)
            except Piuser.DoesNotExist:
                continue
        return returnValue

    def UpdateUser(self, userEntity):
        """
        更新用户
        Args:
            userEntity (Piuser): 用户实体
        Returns:
            returnValue (string): 状态码
            returnMessage (string): 状态信息
        """
        try:
            userEntity.save()
            returnCode = StatusCode.statusCodeDic['OKUpdate']
            returnMessage = FrameworkMessage.MSG0010
            return returnCode,returnMessage
        except:
            returnCode = StatusCode.statusCodeDic['Error']
            returnMessage = FrameworkMessage.MSG0001
            return returnCode, returnMessage

    def GetSearchConditional(self, permissionScopeCode, search, roleIds, enabled, auditStates, departmentId):
        """
        获取SQL查询串
        Args:
            permissionScopeCode (string): 权限码
            search (string): 查询字段
            roleIds     (string[]): 用户角色ID字典
            enabled (string): 启用标志
            auditStates (string): 审核状态
            departmentId (string): 组织机构ID
        Returns:
            returnValue (int): SQL组合查询串
        """
        #easyui search
        whereConditional = 'piuser.DELETEMARK = 0 AND piuser.ISVISIBLE = 1 '
        if enabled:
            whereConditional = whereConditional + ' AND ( piuser.ENABLED = 1 ) '

        if search:
            whereConditional = whereConditional + ' AND ( piuser.USERNAME LIKE \'' + search + '\'' \
                + ' OR piuser.CODE LIKE \'' + search + '\'' \
                + ' OR piuser.REALNAME LIKE \'' + search + '\'' \
                + ' OR piuser.QUICKQUERY LIKE \'' + search + '\'' \
                + ' OR piuser.DEPARTMENTNAME LIKE \'' + search + '\'' \
                + ' OR piuser.DESCRIPTION LIKE \'' + search + '\')'

        if departmentId:
            organizeIds = OrganizeService.GetChildrensById(self, departmentId)
            if len(organizeIds) > 0:
                whereConditional = whereConditional + ' AND (piuser.COMPANYID IN (' + StringHelper.ArrayToList(self, organizeIds, '\'') + ')' \
                    + ' OR piuser.COMPANYID IN (' + StringHelper.ArrayToList(self, organizeIds, '\'') + ')' \
                    + ' OR piuser.DEPARTMENTID IN (' + StringHelper.ArrayToList(self, organizeIds, '\'') + ')' \
                    + ' OR piuser.SUBDEPARTMENTID IN (' + StringHelper.ArrayToList(self, organizeIds, '\'') + ')' \
                    + ' OR piuser.WORKGROUPID IN (' + StringHelper.ArrayToList(self, organizeIds, '\'') + '))'

                whereConditional = whereConditional + ' OR piuser.ID IN (' \
                    + ' SELECT ID' \
                    + ' FROM piuser' \
                    + ' WHERE (piuserorganize.DELETEMARK = 0)' \
                    + ' AND (' \
                    + ' piuserorganize.COMPANYID=' + departmentId + '\' OR ' \
                    + ' piuserorganize.SUBCOMPANYID=' + departmentId + '\' OR ' \
                    + ' piuserorganize.DEPARTMENTID=' + departmentId + '\' OR ' \
                    + ' piuserorganize.SUBDEPARTMENTID=' + departmentId + '\' OR ' \
                    + ' piuserorganize.WORKGROUPID=' + departmentId + '\'))'

        if  auditStates:
            whereConditional = whereConditional + ' AND (piuser.AUDITSTATUS=\'' + auditStates + '\')'

        if roleIds:
            roles = StringHelper.ArrayToList(self, roleIds, '\'')
            whereConditional = whereConditional + ' AND (piuser.ID IN ( SELECT USERID FROM piuserrole WHERE ROLEID IN (' + roles + ')))'

        return whereConditional


    def Searchs(self, permissionScopeCode, search, roleIds, enabled, audiStates, departmentId):
        """
        查询用户
        Args:
            permissionScopeCode (string): 权限码
            search (string): 查询字段
            roleIds     (string[]): 用户角色
            enabled (string): 启用标志
            auditStates (string): 审核状态
            departmentId (string): 组织机构ID
        Returns:
            returnValue (List): 用户列表
        """
        userList = []
        sqlQuery = 'select piuser.*,piuserlogon.FIRSTVISIT,piuserlogon.PREVIOUSVISIT,piuserlogon.LASTVISIT,piuserlogon.IPADDRESS,piuserlogon.MACADDRESS,piuserlogon.LOGONCOUNT,piuserlogon.USERONLINE,piuserlogon.CHECKIPADDRESS,piuserlogon.MULTIUSERLOGIN FROM PIUSER LEFT OUTER JOIN PIUSERLOGON ON PIUSER.ID = PIUSERLOGON.ID '
        whereConditional = UserSerivce.GetSearchConditional(self,permissionScopeCode, search, roleIds, enabled, audiStates, departmentId)
        sqlQuery = sqlQuery + " WHERE " + whereConditional
        sqlQuery = sqlQuery + " ORDER BY piuser.SORTCODE"
        userList = DbCommonLibaray.executeQuery(self, sqlQuery)
        return userList

    def Search(self, searchValue, auditStatus, roleIds):
        """
        查询用户
        Args:
            searchValue (string): 查询字段
            auditStatus (string): 审核状态
            roleIds     (string[]): 用户角色ID字典
        Returns:
            returnValue (int): 影响行数
        """
        returnValue = UserSerivce.Searchs(self, '', searchValue, roleIds, None,   auditStatus, '')
        return returnValue



    def SetUserAuditStates(self, ids, auditStates):
        """
        设置用户审核状态
        Args:
            ids (string[]): 主键数组
            auditStates (string): 审核状态
        Returns:
            returnValue (int): 影响行数
        """
        returnValue = Piuser.objects.filter(id__in=ids).update(auditstatus = auditStates)
        if auditStates == AuditStatus.AuditPass:
            returnValue = Piuser.objects.filter(id__in=ids).update(enable=1)
        if auditStates == AuditStatus.AuditReject:
            returnValue = Piuser.objects.filter(id__in=ids).update(enable=0)
        return returnValue

    def Delete(self, id):
        """
        单个删除用户
        Args:
            id (string): 主键
        Returns:
            returnValue (True or False): 删除结果
        """
        try:
            #已删除用户Piuser表中的DELETEMARK设置为1
            try:
                user = Piuser.objects.get(id=id)
            except Piuser.DoesNotExist as e:
                return False
            user.deletemark = 1
            user.save()
            #用户已经被删除的员工的UserId设置为Null
            Pistaff.objects.filter(userid__in=Piuser.objects.filter(deletemark=1)).update(userid=None)
            UserPermission.ClearUserPermissionByUserId(self, id)
            return True
        except Exception as e:
            print(e)
            return False


    def BatchDelete(self, ids):
        pass

    def SetDeleted(self, ids):
        pass

    def BatchSave(self, dataTable):
        pass

    def GetCompanyUser(self):
        pass

    def GetDepartmentUser(self):
        pass

    def GetDepartmentUser(self, departmentId, containChildren):
        pass

    def GetListByDepartment(self, departmentId, containChildren):
        pass