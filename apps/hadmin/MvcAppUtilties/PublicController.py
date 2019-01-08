# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2019/1/8 14:42'

from apps.bizlogic.service.permission.PermissionService import PermissionService
from apps.hadmin.MvcAppUtilties.CommonUtils import CommonUtils

class PublicController(object):

    def IsAuthorized(response, request, permissionItemCode, permissionItemName = None):
        """
        是否有相应的权限
        Args:
            permissionItemCode (string): 权限编号
            permissionItemName (string): 权限名称
        Returns:
            returnValue (bool): 是否有权限
        """
        isAuthorized = PermissionService.IsAuthorizedByUserId(PublicController, CommonUtils.Current(response, request).Id, permissionItemCode, permissionItemName)
        return isAuthorized
