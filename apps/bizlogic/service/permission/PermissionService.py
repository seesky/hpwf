# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2018/12/12 8:14'

from apps.bizlogic.models import Piuser
from apps.bizlogic.service.base.UserRoleService import UserRoleService
from apps.utilities.message.DefaultRole import DefaultRole
from apps.bizlogic.models import Pirole
from apps.bizlogic.models import Pipermissionitem
from django.db.models import Q
from apps.bizlogic.models import Pipermission
from apps.bizlogic.models import Piuserrole
from apps.utilities.publiclibrary.SystemInfo import SystemInfo
from apps.bizlogic.service.base.UserOrganizeSerivce import UserOrganizeService

class PermissionService(object):

    def IsInRole(self, userId, roleName):
        """
        指定用户是否在指定的角色里
        Args:
            userId (string): 用户主键
            roleName (string): 角色名称
        Returns:
            returnValue(True or False): 指定用户是否在指定角色里，true：是，false：否
        """
        roleCode = Pirole.objects.get(realname=roleName).code
        returnValue = UserRoleService.UserInRole(self, userId, roleCode)
        return returnValue

    def IsAuthorized(self, userId, permissionItemCode, permissionItemName=None):
        """
        当前用户是否有相应的权限
        Args:
            userId (string): 用户主键
            permissionItemCode (string): 权限编号
            permissionItemName (string): 权限名称
        Returns:
            returnValue(True or False): 是否有权限，true：是，false：否
        """
        return PermissionService.IsAuthorizedByUserId(self, userId, permissionItemCode, permissionItemName)

    def IsAuthorizedByUserId(self, userId, permissionItemCode, permissionItemName=None):
        returnValue = False
        user = Piuser.objects.get(id=userId)
        returnValue = PermissionService.IsAdministrator(self, user)

        if not returnValue:
            returnValue = PermissionService.CheckPermissionByUser(self, userId, permissionItemCode, permissionItemName)
        return returnValue

    def IsAuthorizedByRoleId(self, roleId, permissionItemCode):
        pass

    def IsAdministrator(self, entity):
        """
        当前用户是否超级管理员
        Args:
            userInfo (UserInfo): 用户
        Returns:
            returnValue(True or False): 当前用户是否为超级管理员，true：是，false：否
        """
        returnValue = False
        userEntity = Piuser.objects.get(id=entity.id)
        if userEntity.id == 'Administrator':
            return True
        if userEntity.code and userEntity.code == 'Administrator':
            return True
        if userEntity.username and userEntity.username == 'Administrator':
            return True

        #TODO:if (this.UserInfo == null) return false;

        #用户的默认角色是超级管理员
        roleEntity = None
        if userEntity.roleid:
            roleIds = UserRoleService.GetRoleIds(self, userEntity.id)
            for tmpid in roleIds:
                if tmpid == DefaultRole.Administrators:
                    return True
                roleEntity = Pirole.objects.get(id=tmpid)
                if roleEntity.code and roleEntity.code == DefaultRole.Administrators:
                    return True
        return False

    def IsAdministratorByUserId(self, userId):
        pass

    def GetPermissionDT(self):
        pass

    def GetPermissionDTByUserId(self, userId):
        pass

    def IsModuleAuthorized(self, moduleCode):
        pass

    def IsModuleAuthorizedByUserId(self, userId, moduleCode):
        pass

    def GetPermissionScopeByUserId(self, userId, permissionItemCode):
        pass

    def CheckUserOrganizePermission(self, userId, permissionItemId, organizeIds):
        if organizeIds.count() == 0:
            return False
        returnValue = Pipermission.objects.filter(Q(resourcecategory='PIORGANIZE') & Q(resourceid__in=organizeIds) & Q(enabled=1) & Q(deletemark=0) & Q(permissionid=permissionItemId))
        return returnValue > 0

    def CheckUserRolePermission(self, userId, permissionItemId):
        '''
        var sqlQuery = " SELECT COUNT(1) "
                            + "   FROM " + PiPermissionTable.TableName
                            + "  WHERE " + "(" + PiPermissionTable.FieldResourceCategory + " = '" + PiRoleTable.TableName + "') "
                            + "        AND (" + PiPermissionTable.FieldEnabled + " = 1 "
                            + "        AND  " + PiPermissionTable.FieldDeleteMark + " = 0) "
                            + "        AND (" + PiPermissionTable.FieldResourceId + " IN ( "
                                                + " SELECT " + PiUserRoleTable.FieldRoleId
                                                + "   FROM " + PiUserRoleTable.TableName
                                                + "  WHERE " + PiUserRoleTable.FieldUserId + " = '" + userId + "' "
                                                + "        AND " + PiUserRoleTable.FieldEnabled + " = 1 "
                                                + "        AND " + PiUserRoleTable.FieldDeleteMark + " = 0 "
                                                + "  UNION ALL "
                                                + " SELECT " + PiUserTable.FieldRoleId
                                                + "   FROM " + PiUserTable.TableName
                                                + "  WHERE " + PiUserTable.FieldId + " = '" + userId + "'"
                                                + ") ) "
                            + "        AND (" + PiPermissionTable.FieldPermissionId + " = '" + permissionItemId + "') ";
        '''
        returnValue = Pipermission.objects.filter(Q(resourcecategory='PIROLE') & Q(enabled=1) & Q(deletemark=0) & Q(permissionid=permissionItemId) \
                                                  & Q(resourceid__in=Piuser.objects.filter(id=userId).values_list('roleid', flat=True).union(Piuserrole.objects.filter(Q(userid=userId) & Q(enabled=1) & Q(deletemark=0)).values_list('roleid',flat=True))))

        return returnValue.count() > 0

    def CheckUserPermission(self, userId, permissionItemId):
        return PermissionService.CheckResourcePermission(self, 'PIUSER', userId, permissionItemId)

    def CheckResourcePermission(self, resourceCategory, resourceId, permissionItemId):
        """
        是否有权限
        Args:
            resourceCategory (string):
            resourceId (string):
            permissionItemId (string):
        Returns:
            returnValue(True or False): 是否有权限
        """
        returnValue = Pipermission.objects.filter(Q(resourcecategory=resourceCategory) & Q(enabled=1) & Q(deletemark=0) & Q(resourceid=resourceId) & Q(permissionid=permissionItemId))
        return returnValue.count() > 0

    def CheckPermissionByUser(self, userId, permissionItemCode, permissionItemName = None):
        """
        是否有相应的权限
        Args:
            userId (string): 用户主键
            permissionItemCode (string): 权限编号
            permissionItemName (string): 权限名称
        Returns:
            returnValue(True or False): 是否有权限
        """
        #若不存在就需要自动能增加一个操作权限项
        permissionItemEntity = None
        try:
            permissionItemEntity = Pipermissionitem.objects.get(Q(code=permissionItemCode) & Q(fullname=permissionItemName))
        except Pipermissionitem.DoesNotExist as e:
            permissionItemEntity = Pipermissionitem()
            permissionItemEntity.code = permissionItemCode
            permissionItemEntity.fullname = permissionItemName
            permissionItemEntity.save()
            # 没有找到相应的权限
            return False

        #先判断用户类别
        user = Piuser.objects.get(id = userId)
        if PermissionService.IsAdministrator(self, user):
            return True

        returnValue = False

        #用户管理员拥有所有的系统权限，不需要授予
        if UserRoleService.UserInRole(self, user.id, 'UserAdmin'):
            return True

        #业务管理员拥有所有的业务(应用）权限，不需要授予
        if permissionItemEntity.categorycode and permissionItemEntity.categorycode == 'Application':
            if UserRoleService.UserInRole(self, user.id, 'Admin'):
                return True

        #判断用户权限
        if PermissionService.CheckUserPermission(self, userId, permissionItemEntity.id):
            return True

        #判断用户角色权限
        if PermissionService.CheckUserRolePermission(self, userId, permissionItemEntity.id):
            return True

        #判断用户组织机构权限，这里有开关是为了提高性能用的，
        #下面的函数接着还可以提高性能，可以进行一次判断就可以了，其实不用执行4次判断，浪费I/O，浪费性能。
        if SystemInfo.EnableOrganizePermission:
            organizeIds = UserOrganizeService.GetAllOrganizeIds(self, userId)
            if PermissionService.CheckUserOrganizePermission(self, userId, permissionItemEntity.id, organizeIds):
                return True

        return False



