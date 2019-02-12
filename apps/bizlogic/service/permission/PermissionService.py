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
from apps.bizlogic.service.base.ModuleService import ModuleService
from apps.bizlogic.service.base.PermissionScopeService import PermissionScopeService
import uuid,datetime

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
        returnValue = PermissionService.IsAdministrator(user)

        if not returnValue:
            returnValue = PermissionService.CheckPermissionByUser(self, userId, permissionItemCode, permissionItemName)
        return returnValue

    def IsAuthorizedByRoleId(self, roleId, permissionItemCode):
        """
        指定角色是否有相应的权限
        Args:
            roleId (string): 角色主键
            permissionItemCode (string): 权限编号
        Returns:
            returnValue(True or False): 是否有权限，true：是，false：否
        """
        returnValue = False
        returnValue = roleId == 'Administrators'
        if not returnValue:
            permissionItemId = Pipermissionitem.objects.get(permissionitemcode=permissionItemCode).id
            #判断当前判断的权限是否存在，否则很容易出现前台设置了权限，后台没此项权限
            #需要自动的能把前台判断过的权限，都记录到后台来
            if not permissionItemId:
                return False

            role = Pipermission.objects.filter(Q(resourcecategory='PIROLE') & Q(enabled=1) & Q(resourceid=roleId) & Q(permissionid=permissionItemId))
            return len(role) > 0

    def IsAdministrator(entity):
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
            roleIds = UserRoleService.GetRoleIds(userEntity.id)
            for tmpid in roleIds:
                if tmpid == DefaultRole.Administrators:
                    return True
                roleEntity = Pirole.objects.get(id=tmpid)
                if roleEntity.code and roleEntity.code == DefaultRole.Administrators:
                    return True
        return False

    def IsAdministratorByUserId(self, userId):
        """
        指定用户是否超级管理员
        Args:
            userId (string): 用户
        Returns:
            returnValue(True or False): 是否超级管理员，true：是，false：否
        """
        returnValue = False
        userEntity = Piuser.objects.get(id=userId)
        return PermissionService.IsAdministrator(userEntity)

    def GetPermissionDTByUserId(self, userId):
        """
        获得指定用户的所有权限列表
        Args:
            userId (string): 用户
        Returns:
            returnValue(Pipermission): 权限列表
        """
        if PermissionService.IsAdministrator(self, Piuser.objects.get(id=userId)):
            return Pipermission.objects.all()
        else:
            #用户的权限
            q1 = Pipermission.objects.filter(Q(enabled=1) & Q(id__in=Pipermission.objects.filter(Q(resourcecategory='PIUSER') & Q(enabled=1) & Q(resourceid=userId))))
            #角色的权限
            q2search1 = Piuserrole.objects.filter(Q(userid=userId) & Q(enabled=1)).values_list('roleid', flat=True)
            q2search2 = Piuser.objects.filter(id=userId).values_list('roleid', flat=True)
            q2 =Pipermission.objects.filter(Q(resourcecategory='PIROLE') & Q(enabled=1) & Q(resourceid__in=q2search1.union(q2search2)))
            returnValue = q1.union(q2)
            return returnValue

    def IsModuleAuthorizedByUserId(self, userId, moduleCode):
        """
        指定用户是否对某个模块有相应的权限
        Args:
            userId (string): 用户
            moduleCode (string): 模块编码
        Returns:
            returnValue(True or False): 是否有权限，true：是，false：否
        """
        returnValue = False
        userEntity = Piuser.objects.get(id=userId)
        returnValue = PermissionService.IsAdministrator(self, userEntity)
        if not returnValue:
            dateTable = ModuleService.GetDTByUser(self, userId)
            for module in dateTable:
                if module.code == moduleCode:
                    returnValue = True
        return returnValue


    def GetPermissionScopeByUserId(self, userId, permissionItemCode):
        """
        获得指定用户的数据权限范围
        Args:
            userId (string): 用户
            moduleCode (string): 模块编码
        Returns:
            returnValue(True or False):
        """
        returnValue = PermissionScopeService.GetUserPermissionScope(self, userId, permissionItemCode)
        return returnValue

    def CheckUserOrganizePermission(self, userId, permissionItemId, organizeIds):
        if len(organizeIds) == 0:
            return False
        returnValue = Pipermission.objects.filter(Q(resourcecategory='PIORGANIZE') & Q(resourceid__in=organizeIds) & Q(enabled=1) & Q(deletemark=0) & Q(permissionid=permissionItemId))
        return len(returnValue) > 0

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

        return len(returnValue) > 0

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
        return len(returnValue) > 0

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

            permissionItemEntity = Pipermissionitem.objects.get(Q(code=permissionItemCode))
        except Pipermissionitem.DoesNotExist as e:
            if not permissionItemName:
                permissionItemName = permissionItemCode
            permissionItemEntity = Pipermissionitem()
            permissionItemEntity.id = uuid.uuid4()
            permissionItemEntity.code = permissionItemCode
            permissionItemEntity.fullname = permissionItemName
            permissionItemEntity.categorycode = "Application"
            permissionItemEntity.parentid = None
            permissionItemEntity.moduleid = None
            permissionItemEntity.isscope = 0
            permissionItemEntity.ispublic = 0
            permissionItemEntity.allowdelete = 1
            permissionItemEntity.allowedit = 1
            permissionItemEntity.enabled = 1
            permissionItemEntity.deletemark = 0
            permissionItemEntity.createon = datetime.datetime.now()
            permissionItemEntity.modifiedon = permissionItemEntity.createon
            permissionItemEntity.save()
            # 没有找到相应的权限
            return False

        #先判断用户类别
        user = Piuser.objects.get(id = userId)
        if PermissionService.IsAdministrator(user):
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



