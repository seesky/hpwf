# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2018/12/11 15:55'

from apps.bizlogic.models import Pipermission

from django.db.models import Q

class ModuleService(object):

    def GetDT(self):
        pass

    def GetDTByCondition(self, condition):
        pass

    def GetList(self):
        pass

    def GetDTByIds(self, ids):
        pass

    def GetEntity(self):
        pass

    def GetFullNameByCode(self, code):
        pass

    def Add(self, moduleEntity, statusCode, statusMessage):
        pass

    def Update(self, moduleEntity, statusCode, statusMessage):
        pass

    def GetDTByParent(self, parentId):
        pass

    def Delete(self, id):
        pass

    def BatchDelete(self, ids):
        pass

    def SetDeleted(self, ids):
        pass

    def MoveTo(self, moduleId, parentId):
        pass

    def BatchMoveTo(self, moduleIds, parentId):
        pass

    def BatchSave(self, dataTable):
        pass

    def SetSortCode(self, ids):
        pass

    def GetPermissionDT(self, moduleId):
        pass

    def GetIdsByPermission(self, permissionItemId):
        pass

    def BatchAddPermissions(self, moduleId, permissionItemIds):
        pass

    def BatchAddModules(self, permissionItemId, moduleIds):
        pass

    def BatchDeletePermissions(self, moduleId, permissionItemIds):
        pass

    def BatchDeleteModules(self, permissionItemId, modulesIds):
        pass

    def GetPermissionIds(self, moduleId):
        returnValue = Pipermission.objects.filter(Q(resourcecategory='PIMODULE') & Q(resourceid=moduleId) & Q(deletemark=0))
        return returnValue