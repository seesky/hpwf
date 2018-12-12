# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2018/12/12 8:14'

def IsInRole(userId, roleName):
    pass

def IsAuthorized(permissionItemCode, permissionItemName=None):
    pass

def IsAuthorizedByUserId(userId, permissionItemCode, permissionItemName=None):
    pass

def IsAuthorizedByRoleId(roleId, permissionItemCode):
    pass

def IsAdministrator():
    pass

def IsAdministratorByUserId(userId):
    pass

def GetPermissionDT():
    pass

def GetPermissionDTByUserId(userId):
    pass

def IsModuleAuthorized(moduleCode):
    pass

def IsModuleAuthorizedByUserId(userId, moduleCode):
    pass

def GetPermissionScopeByUserId(userId, permissionItemCode):
    pass