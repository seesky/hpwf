# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2018/12/20 14:41'

from django.db.models import Q

from apps.bizlogic.models import Pipermission
#from apps.bizlogic.service.base.UserRoleService import UserRoleService

from apps.bizlogic.models import Pimodule
from apps.bizlogic.models import Piuser
from apps.bizlogic.models import Piuserrole
from apps.bizlogic.models import Pirole
from apps.bizlogic.service.base.PermissionScopeService import PermissionScopeService

class ModulePermission(object):

    def GetPermissionIds(self, moduleId):
        returnValue = Pipermission.objects.filter(Q(resourcecategory='PIMODULE') & Q(resourceid=moduleId) & Q(deletemark=0)).values_list('permissionid')
        return returnValue

    def GetModuleIds(self, permissionItemId):
        returnValue = Pipermission.objects.filter(
            Q(resourcecategory='PIPERMISSION') & Q(permissionid=permissionItemId) & Q(deletemark=0)).values_list('resourceid')
        return returnValue

    def Add(self, moduleId, permissionItemId):
        returnValue = 0
        try:
            Pipermission.objects.get(Q(resourcecategory='PIMODULE') & Q(resourceid=moduleId) & Q(permissionid=permissionItemId) & Q(deletemark=0))
            return returnValue
        except Pipermission.DoesNotExist as e:
            permission = Pipermission()
            permission.resourceid = moduleId
            permission.resourcecategory = Pipermission._meta.db_table
            permission.enabled = 1
            permission.deletemark = 0
            permission.permissionid = permissionItemId
            permission.save()
            returnValue = returnValue + 1
            return returnValue

    def AddsI(self, moduleId, permissionItemIds):
        returnValue = 0
        for item in permissionItemIds:
            ModulePermission.Add(self, moduleId, permissionItemIds)
            returnValue = returnValue + 1
        return returnValue

    def AddsM(self, moduleIds, permissionItemId):
        returnValue = 0
        for module in moduleIds:
            ModulePermission.Add(module, permissionItemId)
            returnValue = returnValue + 1
        return returnValue

    def Delete(self, moduleId, permissionItemId):
        returnValue = Pipermission.objects.filter(Q(resourcecategory='PIMODULE') & Q(resourceid=moduleId) & Q(permissionid=permissionItemId)).delete()
        return returnValue

    def DeletesM(self, moduleIds, permissionItemId):
        returnValue = 0
        for module in moduleIds:
            returnValue = returnValue + ModulePermission.Delete(self, moduleIds, permissionItemId)
        return returnValue

    def DeletesI(self, moduleId, permissionItemIds):
        returnValue = 0
        for item in permissionItemIds:
            returnValue = returnValue + ModulePermission.Delete(self, moduleId, item)
        returnValue

    def GetDTByPermission(self, userId, permissionItemScopeCode):
        #这里需要判断,是系统权限？
        isRole = False
        isRole = ModulePermission.UserInRole(self, userId, "UserAdmin")
        #用户管理员
        if isRole:
            returnValue = Pimodule.objects.filter(Q(category='System') & Q(deletemark=0) & Q(enabled=1)).order_by('sortcode')
            return returnValue

        isRole = ModulePermission.UserInRole(self, userId, "Admin")
        if isRole:
            returnValue = Pimodule.objects.filter(Q(category='Application') & Q(deletemark=0) & Q(enabled=1)).order_by(
                'sortcode')
            return returnValue

        moduleIds = PermissionScopeService.GetTreeResourceScopeIds(self, userId, 'PIMODULE', permissionItemScopeCode, True)
        returnValue = Pimodule.objects.filter(Q(id__in=moduleIds) & Q(deletemark=0) & Q(enabled=1))
        return returnValue

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
        roleIds = ModulePermission.GetAllRoleIds(self, userId)
        if roleId in roleIds:
            return True
        else:
            return False

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



