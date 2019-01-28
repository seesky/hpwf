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
from apps.bizlogic.models import Piuserrole
from apps.bizlogic.service.base.UserService import UserSerivce
from apps.bizlogic.service.base.UserRoleService import UserRoleService


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
        returnValue = None
        try:
            # for role in Pirole.objects.all():
            #     returnValue.append(role)
            returnValue = Pirole.objects.filter(deletemark=0)
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

    def GetDtByPage(self, pageSize=20, whereConditional="", order=""):
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
        return returnValue

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
        # returnValue = []
        # for id in ids:
        #     try:
        #         role = Pirole.objects.get(id=id)
        #         returnValue.append(role)
        #     except Pirole.DoesNotExist:
        #         continue
        returnValue = Pirole.objects.filter(Q(id__in=ids) & Q(deletemark=0))
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
        Args:
            organizeId (string) : 组织机构主键
            showUser (bool) : 显示用户
        Returns:
            returnValue (Pirole[]): 角色列表
        """
        dtRole = Pirole.objects.filter(Q(organizeid=organizeId) & Q(deletemark=0)).order_by('sortcode')
        if showUser:
            username = ''
            dataTableUser = UserSerivce.GetDT(self)
            for role in dtRole:
                userIds = UserSerivce.GetUserIdsInRole(self, role.id)
                if userIds:
                    for userid in userIds:
                        username = username + Piuser.objects.get(id=userid).realname + ', '
                if username:
                    role.users = username[:-2]
                username = ""
        return dtRole


    def GetApplicationRole(self):
        """
        获取业务角色列表
        Args:
        Returns:
            returnValue (Pirole[]): 业务角色列表
        """
        returnValue = Pirole.objects.filter(Q(deletemark=0) & Q(category='ApplicationRole'))
        return returnValue

    def BatchSave(self, entites):
        """
        批量保存
        Args:
            dataTable (Piuser[]): 用户列表
        Returns:
            returnValue (True or False): 保存结果
        """
        try:
            for role in entites:
                role.save()
            return True
        except:
            return False

    def Delete(self, id):
        """
        单个删除角色
        Args:
            id (string): 主键
        Returns:
            returnValue (True or False): 删除结果
        """
        returnValue = 0
        returnValue = returnValue + Piuserrole.objects.filter(roleid=id).delete()
        returnValue = returnValue + Pirole.objects.filter(Q(id=id) & Q(allowdelete=1)).delete()
        return returnValue

    def BatchDelete(self, ids):
        """
        批量删除
        Args:
            ids (string[]): 主键列表
        Returns:
            returnValue (True or False): 删除结果
        """
        returnValue = 0
        for id in ids:
            returnValue = returnValue + RoleService.Delete(self, id)
        return returnValue

    def SetDeleted(self, ids):
        """
        批量逻辑删除角色
        Args:
            ids (string[]): 主键列表
        Returns:
            returnValue (True or False): 删除结果
        """
        #TODO:此处还应该把角色相应的权限，所拥有的用户等也做统一处理。
        returnValue = Pirole.objects.filter(Q(id__in=ids)).update(deletemark=1)
        return returnValue

    def EliminateRoleUser(self, roleId):
        """
        移除角色用户关联
        Args:
            id (string): 角色主键
        Returns:
            returnValue (int): 移除影响行数
        """
        returnValue = 0
        returnValue = UserRoleService.EliminateRoleUser(self, roleId)
        return returnValue

    def GetRoleUserIds(self, roleId):
        """
        获得角色中的用户主键
        Args:
            roleId (string): 角色主键
        Returns:
            returnValue (string[]): 用户主键列表
        """
        returnValue = UserRoleService.GetUserIds(self, roleId)
        return returnValue

    def AddUserToRole(userInfo, roleId, addUserIds):
        """
        用户添加到角色
        Args:
            roleId (string): 角色主键
            addUserIds (string): 用户主键列表
        Returns:
            returnValue (int): 影响行数
        """
        returnValue = UserRoleService.AddToRolesU(userInfo, addUserIds, roleId)
        return returnValue

    def RemoveUserFromRole(userInfo, userIds, roleId):
        """
       将用户从角色中移除
       Args:
           userIds (string[]): 角色主键列表
           roleId (string): 角色主键
       Returns:
           returnValue (int): 影响行数
       """
        returnValue = UserRoleService.RemoveFromRoleU(userInfo, userIds, roleId)
        return returnValue

    def ClearRoleUser(self, roleId):
        """
       清除角色用户关联
       Args:
           roleId (string): 角色主键
       Returns:
           returnValue (int): 影响行数
       """
        pass

    def SetUsersToRole(self, roleId, userIds):
        pass

    def ResetSortCode(self, organizeId):
        pass

    def MoveTo(self, id, targetOrganizedId):
        try:
            role = Pirole.objects.get(id=id)
        except Pirole.DoesNotExist as e:
            return False

        try:
            role.organizeid = targetOrganizedId
            role.save()
            return True
        except:
            return False