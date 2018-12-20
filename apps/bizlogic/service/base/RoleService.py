# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2018/12/11 16:29'

from apps.bizlogic.models import Pirole

from django.db.utils import DatabaseError
from django.db.transaction import TransactionManagementError
from django.core.paginator import Paginator
from django.db.models import Q

from utilities.message.StatusCode import StatusCode
from utilities.message.FrameworkMessage import FrameworkMessage
from utilities.publiclibrary.DbCommonLibaray import DbCommonLibaray
from apps.bizlogic.models import Piuser
from apps.bizlogic.service.base.UserService import UserSerivce

class RoleService(object):
    """
    新增实体
    """
    def Add(self, entity):
        """
        用户名是否重复
        Args:
            entity (Pirole):
        Returns:
            returnValue(bool): 新增结果
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
        pass

    def Update(self, entity):
        """
        更新实体
        Args:
            entity (Piuser): 用户实体
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

    def GetDT(self):
        """
        取得角色列表
        Args:
        Returns:
            returnValue (List): 角色列表
        """
        returnValue = []
        try:
            for role in Pirole.objects.all():
                returnValue.append(role)
            return returnValue
        except DatabaseError as e:
            return returnValue
        except TransactionManagementError as e:
            return returnValue

    def GetList(self):
        """
        取得角色列表
        Args:
        Returns:
            returnValue (List): 角色列表
        """
        returnValue = []
        try:
            for role in Pirole.objects.all():
                returnValue.append(role)
            return returnValue
        except DatabaseError as e:
            return returnValue
        except TransactionManagementError as e:
            return returnValue

    def GetDtByPage(self, recordCount, pageSize=20, whereConditional="", order=""):
        """
        取得角色列表
        Args:
            whereConditional (string): 查询字段
            pageSize (int): 每页显示
            order (string): 排序
        Returns:
            recordCount (int): 角色数
            returnValue (List): 角色分页列表

        """
        if not whereConditional:
            if not order:
                whereConditional = 'SELECT * FROM ' + Pirole._meta.db_table + ' WHERE deletemark = 0'
            else:
                whereConditional = 'SELECT * FROM ' + Pirole._meta.db_table + ' WHERE deletemark = 0 ORDER BY ' + order
        else:
            if not order:
                'SELECT * FROM ' + Pirole._meta.db_table + ' WHERE ' + whereConditional + ' AND deletemark = 0'
            else:
                whereConditional = 'SELECT * FROM ' + Pirole._meta.db_table + ' WHERE ' + whereConditional + ' AND deletemark = 0 ORDER BY ' + order
        staffList = DbCommonLibaray.executeQuery(self, whereConditional)
        returnValue = Paginator(staffList, pageSize)
        recordCount = returnValue.count
        return recordCount,returnValue

    def GetEntity(self, id):
        """
        获取角色实体
        Args:
            id (string): 角色主键
        Returns:
            returnValue (Pirole or None): 员工实体
        """
        try:
            role = Pirole.objects.get(id=id)
            return role
        except Pirole.DoesNotExist:
            return None

    def GetDTByIds(self, ids):
        """
        按主键获取员工列表
        Args:
            ids (List[string]): 主键数组
        Returns:
            returnValue (List): 用户列表
        """
        returnValue = []
        for id in ids:
            try:
                role = Pirole.objects.get(id=id)
                returnValue.append(role)
            except Pirole.DoesNotExist:
                continue
        return returnValue

    def GetDTByValues(self, valueDic):
        """
        按键值对获取列表
        valueDic = {key:value, key:value, ...}
        Args:
            valueDic (Dic{key:value}): 参数和值对
        Returns:
            returnValue (Pioranize[]): 角色列表
        """
        q = Q()
        for i in valueDic:
            q.add(Q(**{i: valueDic[i]}), Q.AND)
        returnValue = Pirole.objects.filter(q)
        return returnValue

    def GetDTByOrganize(self, organizeId, showUser=True):
        """
        按组织机构获取角色列表
        valueDic = {key:value, key:value, ...}
        Args:
            organizeId (string) : 组织机构主键
            showUser (bool) : 显示用户
        Returns:
            returnValue (Pirole[]): 角色列表
        """
        dtRole = Pirole.objects.filter(Q(organizeid=organizeId) & Q(deletemark=0))
        if showUser:
            username = ''
            dataTableUser = UserSerivce.GetDT(self)
            for role in dtRole:
                userIds = UserSerivce.GetUserIdsInRole(self, role.id)
                if userIds:
                    for userid in userIds:
                        username = username + Piuser.objects.get(id=userid).realname + ', '
                if username:
                    role.Users = username
        return dtRole


    def GetApplicationRole(self):
        pass

    def BatchSave(self, entites):
        pass

    def Delete(self, id):
        pass

    def BatchDelete(self, ids):
        pass

    def SetDeleted(self, ids):
        pass

    def EliminateRoleUser(self, roleId):
        pass

    def GetRoleUserIds(self, roleId):
        pass

    def AddUserToRole(self, roleId, addUserIds):
        pass

    def RemoveUserFromRole(roleId, userIds):
        pass

    def ClearRoleUser(roleId):
        pass

    def SetUsersToRole(roleId, userIds):
        pass

    def ResetSortCode(organizeId):
        pass

    def MoveTo(id, targetOrganizedId):
        pass