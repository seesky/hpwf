# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2019/1/8 16:15'

from apps.hadmin.MvcAppUtilties.AjaxOnly import AjaxOnly
from apps.hadmin.MvcAppUtilties.LoginAuthorize import LoginAuthorize

from apps.bizlogic.service.base.OrganizeService import OrganizeService
from apps.bizlogic.service.permission.ScopPermission import ScopPermission

from apps.utilities.publiclibrary.SystemInfo import SystemInfo
from apps.utilities.message.OrganizeCategory import OrganizeCategory
from apps.hadmin.MvcAppUtilties.CommonUtils import CommonUtils

from django.db.models import Q
from django.http.response import HttpResponse

from django.core import serializers

import json

def GetOrganizeScope(userInfo, permissionItemScopeCode, isInnerOrganize):
    """
    获取组织机构权限域数据
    Args:
    Returns:
    """
    if userInfo.IsAdministrator or (not permissionItemScopeCode) or (not SystemInfo.EnableUserAuthorizationScope):
        dataTable = OrganizeService.GetDT(object)
    else:
        dataTable = ScopPermission.GetOrganizeDTByPermissionScope(None, userInfo, userInfo.Id, permissionItemScopeCode)

    if isInnerOrganize:
        dataTable = dataTable.filter(Q(isinnerorganize='1')).order_by('sortcode')
    return dataTable

def GroupJsondata(groups, parentId):
    treeLevel = 0
    sb = ""
    list = []
    for g in groups:
        if g.parentid == parentId:
            list.append(g)
    for g in list:
        treeLevel = treeLevel + 1
        #jsons = json.dumps(g)
        #jsons = serializers.serialize('json', g)
        jsons = g.toJSON()
        jsons = jsons.rstrip('}')
        sb = sb + jsons
        if g.category and g.category.lower() == OrganizeCategory.OrganizeCategory.get('Company').lower():
            sb = sb + ",\"iconCls\":\"icon16_sitemap\""
        elif g.category and g.category.lower() == OrganizeCategory.OrganizeCategory.get('SubCompany').lower():
            sb = sb + ",\"iconCls\":\"icon16_server\""
        elif g.category and g.category.lower() == OrganizeCategory.OrganizeCategory.get('Department').lower():
            sb = sb + ",\"iconCls\":\"icon16_building\""
        elif g.category and g.category.lower() == OrganizeCategory.OrganizeCategory.get('SubDepartment').lower():
            sb = sb + ",\"iconCls\":\"icon16_ipod\""
        elif g.category and g.category.lower() == OrganizeCategory.OrganizeCategory.get('Workgroup').lower():
            sb = sb + ",\"iconCls\":\"icon16_envelopes\""

        sb = sb + ","

        if treeLevel >= 2 and len(groups.filter(Q(parentid=g.id))) > 0:
            sb = sb + "\"state\":\"closed\","

        sb = sb + "\"children\":["

        if g.id:
            sb = sb + GroupJsondata(groups, g.id)
        sb = sb + "]},"
    sb = sb.rstrip(',')
    return sb

@LoginAuthorize
def GetOrganizeTreeJson(request, isTree = 0):

    if isTree == '1':
        isTree = True
    else:
        isTree = False



    response = HttpResponse()
    dtOrganize = GetOrganizeScope(CommonUtils.Current(response, request), 'Resource.ManagePermission', False)
    dataTable = CommonUtils.CheckTreeParentId(dtOrganize, 'id', 'parentid')
    organizeJson = "[" + GroupJsondata(dtOrganize, "#") + "]"

    if isTree:
        response.content = organizeJson.replace("fullname", "text")
        return response
    else:
        response.content = organizeJson
        return response