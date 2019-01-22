# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2018/12/11 16:17'

import uuid
import datetime

from django.db.models import Q

from apps.bizlogic.models import Piuserrole
from apps.bizlogic.models import Pirole
from apps.bizlogic.models import Piuser

from apps.bizlogic.service.base.UserService import UserSerivce
from apps.utilities.message.DefaultRole import DefaultRole

class UserRoleService(object):

    def GetDTByRole(self, roleId):
        """
        按角色获取用户列表
        Args:
            roleId (string): 角色主键
        Returns:
            returnValue (Piuser[]): 用户列表
        """
        returnValue = Piuser.objects.filter(Q(enabled=1) & Q(deletemark=0) & (Q(roleid=roleId) | Q(id__in=Piuserrole.objects.filter(Q(roleid=roleId) & Q(enabled=1) & Q(deletemark=0)).values_list('userid', flat=True)))).order_by('sortcode')
        return returnValue

    def GetListByRole(self, roleIds):
        """
        按角色获取用户列表
        Args:
            roleIds (string): 角色主键列表
        Returns:
            returnValue (Piuser[]): 用户列表
        """
        returnValue = Piuser.objects.filter(Q(enabled=1) & Q(deletemark=0) &  Q(id__in=Piuserrole.objects.filter(Q(roleid__in=roleIds) & Q(enabled=1) & Q(deletemark=0)).valus_list('userid',flat=True))).order_by( 'sortcode')
        return returnValue

    def GetRoleDT(self, user):
        """
        获取用户的角色列表
        Args:
        Returns:
            returnValue (Pirole[]): 角色列表
        """
        #TODO:此处缺少判断用户是否位管理员的方法，暂时用True代替
        if True:
            dataTable = Pirole.objects.filter(Q(deletemark=0) & Q(enabled=1) & ~Q(code=DefaultRole.Administrators)).order_by('sortcode')
        else:
            dataTable = Pirole.objects.filter(Q(deletemark=0) & Q(enabled=1)).order_by('sortcode')


    def UserInRole(self, userId, roleCode):
        """
        用户是否在某个角色里的判断
        Args:
            userId (string): 用户ID
            roleCode (string): 角色编号
        Returns:
            returnValue (Pirole[]): 角色列表
        """
        returnValue = False
        if not roleCode:
            return False
        roleId = Pirole.objects.get(Q(deletemark=0) & Q(code=roleCode)).id
        if not roleId:
            return False
        roleIds = UserRoleService.GetAllRoleIds(self, userId)
        if roleId in roleIds:
            return True
        else:
            return False

    def SetDefaultRole(self, userId, roleId):
        """
        设置用户的默认角色
        Args:
            userId (string): 用户ID
            roleCode (string): 角色编号
        Returns:
            returnValue (Pirole[]): 影响行数
        """
        returnValue = Piuser.objects.filter(userid=userId).update(roleid=roleId)
        return returnValue

    def BatchSetDefaultRole(self, userIds, roleId):
        """
        设置用户的默认角色
        Args:
            userId (string): 用户ID
            roleCode (string): 角色编号
        Returns:
            returnValue (Pirole[]): 影响行数
        """
        returnValue = Piuser.objects.filter(userid__in=userIds).update(roleid=roleId)

    def GetUserRoleIds(self, userId):
        """
        获取用户角色列表
        Args:
            userId (string): 用户ID
        Returns:
            returnValue (string[]): 角色主键列表
        """
        returnValue = Piuserrole.objects.filter(userid=userId).values_list('id', flat=True)
        return returnValue

    def GetAllUserRoleIds(self, userId):
        """
        获取用户角色列表
        Args:
            userId (string): 用户ID
        Returns:
            returnValue (string[]): 角色主键列表
        """
        returnValue = Piuserrole.objects.filter(userid=userId).values_list('id', flat=True)
        return returnValue

    def AddUserToRole(self, userId, addRoleIds):
        """
       用户添加到角色
       Args:
           userId (string): 用户ID
           addRoleIds (string[]): 角色主键ID
       Returns:
           returnValue (string): 主键
       """
        try:
            Piuserrole.objects.get(Q(userid=userId) & Q(roleid=addRoleIds) & Q(enabled=1) & Q(deletemark=0))
        except Piuserrole.DoesNotExist as e:
            userrole = Piuserrole()
            userrole.userid = userId
            userrole.roleid = addRoleIds
            userrole.enabled = 1
            userrole.deletemark = 0
            userrole.save()
            return userrole.id

    def RemoveUserFromRole(self, userId, removeRoleIds):
        """
       从角色中删除员工
       Args:
           userId (string): 员工主键
           addRoleIds (string): 角色主键
       Returns:
           returnValue (int): 影响行数
       """
        returnValue = Piuserrole.objects.filter(Q(userId=userId) & Q(roleid=removeRoleIds)).delete()
        return returnValue


    def ClearUserRole(self, userId):
        """
       清除用户归属的角色
       Args:
           userId (string): 员工主键
       Returns:
           returnValue (int): 影响行数
       """
        returnValue = Piuserrole.objects.filter(userid=userId).delete()
        return returnValue

    def GetAllRoleIds(self, userId):
        if not userId:
            return []
        else:
            # sqlQuery = 'select roleid from piuser where (id=\'' + userId + '\') AND '
            # sqlQuery = sqlQuery + '(deletemark=0) AND '
            # sqlQuery = sqlQuery + ' (enabled=1) union select roleid from piuserrole where (userid=\'' + userId + '\') AND '
            # sqlQuery = sqlQuery + '(roleid in (select id from pirole where (deletemark = 0 ))) AND (deletemark=0)'

            list1 = Piuser.objects.filter(Q(id=userId) & Q(deletemark=0) & Q(enabled=1)).values_list('roleid', flat=True)
            list2 = Piuserrole.objects.filter(Q(userid=userId) & Q(roleid__in=Pirole.objects.filter(deletemark=0).values('id')) & Q(deletemark=0)).values_list('roleid', flat=True)
            returnValue = list1.union(list2)
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
        returnValue = Piuser.objects.filter(Q(roleid=roleId)).update(roleid=None)
        returnValue = returnValue + Piuserrole.objects.filter(roleid=roleId).delete()
        return returnValue

    def GetUserIds(self, roleId):
        """
        获取员工的角色主键数组
        Args:
            roleId (string): 角色主键
        Returns:
            returnValue (int): 用户主键列表
        """
        q1 = Piuser.objects.filter(Q(roleid=roleId) & Q(deletemark=0) & Q(enabled=1)).values_list('id', flat=True)
        q2 = Piuserrole.objects.filter(Q(roleid=roleId) & Q(userid__in=Piuser.objects.filter(deletemark=0).values_list('id', flat=True)) & Q(deletemark=0))
        returnValue = q1.union(q2)
        return returnValue

    def AddToRole(userInfo, userId, roleId):
        """
        加入到角色
        Args:
            userId (string): 用户主键
            roleId (string): 角色主键
        Returns:
            returnValue (int): 影响行数
        """
        returnValue = 0
        try:
            Piuserrole.objects.get(Q(userid=userId) & Q(roleid=roleId) & Q(enabled=1) & Q(deletemark=0))
            return returnValue + 1
        except Piuserrole.DoesNotExist as e:
            userrole = Piuserrole()
            userrole.id = uuid.uuid4()
            userrole.userid = userId
            userrole.roleid = roleId
            userrole.allowedit = 1
            userrole.allowdelete = 1
            userrole.createon = datetime.datetime.now()
            userrole.createby = userInfo.RealName
            userrole.modifiedon = userrole.createon
            userrole.modifiedby = userInfo.RealName
            userrole.enabled = 1
            userrole.deletemark = 0

            userrole.save()
            returnValue = 1
            return returnValue

    def AddToRolesR(self, userId, roleIds):
        returnValue = 0
        for roleid in roleIds:
            returnValue = returnValue + UserRoleService.AddToRole(self, userId, roleid)
        return returnValue

    def AddToRolesU(userInfo, userIds, roleId):
        returnValue = 0
        for userid in userIds:
            returnValue = returnValue + UserRoleService.AddToRole(userInfo, userid, roleId)
        return returnValue

    def RemoveFormRole(userInfo, userId, roleId):
        try:
            Piuserrole.objects.filter(Q(userid=userId) & Q(roleid=roleId)).delete()
            return 1
        except:
            return 0

    def RemoveFromRoleR(self, userId, roleIds):
        returnValue = 0
        for roleid in roleIds:
            returnValue = returnValue + UserRoleService.RemoveFormRole(self, userId, roleid)
        return returnValue

    def RemoveFromRoleU(userInfo, userIds, roleId):
        returnValue = 0
        for userid in userIds:
            returnValue = returnValue + UserRoleService.RemoveFormRole(userInfo, userid, roleId)
        return returnValue

    def ClearRoleUser(self, roleId):
        returnValue = 0
        Piuser.objects.filter(roleid=roleId).update(roleid=None)
        returnValue = returnValue + Piuserrole.objects.filter(roleid=roleId).delete()
        return returnValue

    def GetRoleIds(userId):
        returnValue = Piuserrole.objects.filter(Q(userid=userId) & Q(roleid__in=Pirole.objects.filter(deletemark=0).values_list('id', flat=True)) & Q(deletemark=0)).values_list('roleid',flat=True)
        return returnValue

