# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2018/12/20 14:41'

from django.db.models import Q

from apps.bizlogic.models import Pipermission

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