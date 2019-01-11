# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2018/12/11 16:13'

from apps.bizlogic.models import Piuser
from apps.bizlogic.models import Piuserorganize
from apps.bizlogic.models import Piorganize
from apps.bizlogic.service.base.UserService import UserSerivce
from apps.bizlogic.service.base.UserRoleService import UserRoleService
from apps.bizlogic.service.base.OrganizeService import OrganizeService
from apps.bizlogic.service.base.RoleService import RoleService
from apps.utilities.publiclibrary.DbCommonLibaray import DbCommonLibaray
from django.db.utils import DatabaseError
from django.db.transaction import TransactionManagementError
from django.db.models import Q
from utilities.message.StatusCode import StatusCode
from utilities.message.FrameworkMessage import FrameworkMessage



class UserOrganizeService(object):

    def GetDTByDepartment(self, departmentId, containChildren):
        """
        按部门获取用户列表
        Args:
            departmentId (string): 部门主键
            containChildren (string): 含有子部门
        Returns:
            returnValue (Piuser or None): 用户实体
        """
        if not departmentId:
            #dataTable = Piuser.objects.filter(deletemark=0).order_by('sortcode', flat=True)
            dataTable = UserSerivce.GetDT()
        else:
            dataTable = UserSerivce.GetDepartmentUsers(self, departmentId, containChildren)
        return dataTable

    def GetUserPageDTByDepartment(self, userInfo, permissionScopeCode, searchValue,  enabled, auditStates, roleIds, showRole, userAllInformation, pageIndex=0, pageSize=100, sort=None, departmentId=None):
        #TODO:还需要完善此方法
        if not departmentId:
            departmentId = ''

        myrecordCount = 0
        myrecordCount, dt = UserSerivce.SearchByPage(self, userInfo, permissionScopeCode, searchValue, roleIds, enabled, auditStates, departmentId, pageIndex, pageSize)

        if showRole:
            #这里是获取角色列表
            dataTableRole = RoleService.GetDT(None)
            #友善的显示属于多个角色的功能
            roleName = ''
            for user in dt:
                roleName = ''
                roleIds = UserRoleService.GetRoleIds(user['ID'])
                if roleIds:
                    for i in roleIds:
                        roleName = roleName + dataTableRole.filter(id = i)[0].realname + ", "
                if roleName:
                    roleName = roleName.strip(", ")
                    user['ROLENAME'] = roleName
        return myrecordCount,dt



    def GetUserOrganizeDT(self, userId):
        """
        获得用户的组织机构兼职情况
        Args:
            userId (string): 用户主键
        Returns:
            returnValue (Piorganize[]): 组织结构实体
        """
        sqlQuery = " SELECT PIUSERORGANIZE.* " \
        + "     , PiOrganize1.FULLNAME AS CompanyName " \
        + "     , PiOrganize2.FULLNAME AS SubCompanyName " \
        + "     , PiOrganize3.FULLNAME AS DepartmentName " \
        + "     , PiOrganize4.FULLNAME AS SubDepartmentName " \
        + "     , PiOrganize5.FULLNAME AS WorkGroupName " \
        + " FROM PIUSERORGANIZE LEFT OUTER JOIN " \
        + "     PIORGANIZE PiOrganize1 ON PIUSERORGANIZE.CompanyId = PiOrganize1.Id LEFT OUTER JOIN " \
        + "     PIORGANIZE PiOrganize2 ON PIUSERORGANIZE.SubCompanyId = PiOrganize2.Id LEFT OUTER JOIN " \
        + "     PIORGANIZE PiOrganize3 ON PIUSERORGANIZE.DepartmentId = PiOrganize3.Id LEFT OUTER JOIN " \
        + "     PIORGANIZE PiOrganize4 ON PIUSERORGANIZE.SubDepartmentId = PiOrganize4.Id LEFT OUTER JOIN " \
        + "     PIORGANIZE PiOrganize5 ON PIUSERORGANIZE.WorkgroupId = PiOrganize5.Id  " \
        + " WHERE USERID = '" + userId + "'AND  PIUSERORGANIZE.DELETEMARK = 0 ";

        returnValue = DbCommonLibaray.executeQuery(self, sqlQuery)
        return returnValue

    def AddUserToOrganize(self, userOrganizeEntity):
        """
        把用户添加到组织机构
        Args:
            userEntity (PiUserOrganize): 用户组织机构关系
        Returns:
            returnValue (string): 主键
        """
        try:
            userOrganizeEntity.save()
            returnCode = StatusCode.statusCodeDic['OKAdd']
            returnMessage = FrameworkMessage.MSG0009
            returnValue = userOrganizeEntity.id
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

    def BatchDeleteUserOrganize(self, ids):
        """
        把用户添加到组织机构
        Args:
            ids (string): 主键数组
        Returns:
            returnValue (int): 影响行数
        """
        returnValue = Piuserorganize.objects.filter(id__in=ids).delete()
        return returnValue

    def UserIsInOrganize(self, userId, organizeName):
        returnValue = False
        try:
            organizeId = Piorganize.objects.get(Q(fullname=organizeName) & Q(enabled=1) & Q(deletemark=0)).id
        except Piorganize.DoesNotExist as e:
            organizeId = None
        if not organizeId:
            return returnValue

        organizeIds = UserOrganizeService.GetAllOrganizeIds(self, userId)
        if organizeIds.count == 0:
            return returnValue

        if organizeId in organizeIds:
            return True
        else:
            return False

    def GetAllOrganizeIds(self, userId):
        """
        获取用户的所有所在部门主键数组（包括兼职的部门）
        Args:
            userId (string): 用户主键
        Returns:
            returnValue (string[]): 主键数组
        """
        q1 = Piuser.objects.filter(Q(deletemark=0) & Q(enabled=1) & Q(companyid__isnull=False) & Q(id=userId)).values_list('companyid', flat=True)
        q2 = Piuser.objects.filter(Q(deletemark=0) & Q(enabled=1) & Q(subcompanyid__isnull=False) & Q(id=userId)).values_list('subcompanyid', flat=True)
        q3 = Piuser.objects.filter(Q(deletemark=0) & Q(enabled=1) & Q(departmentid__isnull=False) & Q(id=userId)).values_list('departmentid', flat=True)
        q4 = Piuser.objects.filter(
            Q(deletemark=0) & Q(enabled=1) & Q(subdepartmentid__isnull=False) & Q(id=userId)).values_list('subdepartmentid',
                                                                                                       flat=True)
        q5 = Piuser.objects.filter(
            Q(deletemark=0) & Q(enabled=1) & Q(workgroupid__isnull=False) & Q(id=userId)).values_list('workgroupid',
                                                                                                       flat=True)
        q6 = Piuserorganize.objects.filter(Q(deletemark=0) & Q(enabled=1) & Q(companyid__isnull=False) & Q(userid=userId)).values_list('companyid',
                                                                                                       flat=True)
        q7 = Piuserorganize.objects.filter(
            Q(deletemark=0) & Q(enabled=1) & Q(subcompanyid__isnull=False) & Q(userid=userId)).values_list('subcompanyid',
                                                                                                       flat=True)

        q8 = Piuserorganize.objects.filter(
            Q(deletemark=0) & Q(enabled=1) & Q(departmentid__isnull=False) & Q(userid=userId)).values_list(
            'departmentid',
            flat=True)

        q9 = Piuserorganize.objects.filter(
            Q(deletemark=0) & Q(enabled=1) & Q(subdepartmentid__isnull=False) & Q(userid=userId)).values_list(
            'subdepartmentid',
            flat=True)

        q10 = Piuserorganize.objects.filter(
            Q(deletemark=0) & Q(enabled=1) & Q(workgroupid__isnull=False) & Q(userid=userId)).values_list(
            'workgroupid',
            flat=True)

        #returnValue = q1.union(q2).union(q3).union(q4).union(q5).union(q6).union(q7).union(q8).union(q9).union(q10)
        q = q1.union(q2)
        q = q.union(q3)
        q = q.union(q4)
        q = q.union(q5)
        q = q.union(q6)
        q = q.union(q7)
        q = q.union(q8)
        q = q.union(q9)
        q = q.union(q10)

        returnValue = []

        for user in q:
            returnValue.append(user)
        return returnValue



