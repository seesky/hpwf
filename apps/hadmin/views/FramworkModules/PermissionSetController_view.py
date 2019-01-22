# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2019/1/22 8:02'

from apps.hadmin.MvcAppUtilties.LoginAuthorize import LoginAuthorize
from django.http.response import HttpResponse
from apps.hadmin.MvcAppUtilties.AjaxOnly import AjaxOnly
from django.template import loader ,Context
from apps.hadmin.MvcAppUtilties.CommonUtils import CommonUtils
from apps.bizlogic.service.permission.ResourcePermission import ResourcePermission
from apps.bizlogic.service.base.PermissionItemService import PermissionItemService
from apps.utilities.publiclibrary.StringHelper import StringHelper
import json

def RoleUserSet(request):
    response = HttpResponse()
    tmp = loader.get_template('PermissionSet/RoleUserSet.html')  # 加载模板
    render_content = {}  # 将要渲染到模板的数据
    new_body = tmp.render(render_content)  # 渲染模板
    response.content = new_body  # 设置返回内容
    return response

@LoginAuthorize
def PermissionBacthSet(request):
    response = HttpResponse()
    tmp = loader.get_template('PermissionSet/PermissionBacthSet.html')  # 加载模板
    render_content = {}  # 将要渲染到模板的数据
    new_body = tmp.render(render_content)  # 渲染模板
    response.content = new_body  # 设置返回内容
    return response

@LoginAuthorize
def GetPermissionScopeTargetIds(request):
    try:
        resourceCategory = request.POST['resourceCategory']
        resourceId = request.POST['resourceId']
        targetCategory = request.POST['targetCategory']
    except:
        resourceCategory = None
        resourceId = None
        targetCategory = None

    ids = ResourcePermission.GetPermissionScopeTargetIds(None, resourceCategory, resourceId, targetCategory, "Resource.ManagePermission")
    returnValue = StringHelper.ArrayToList(None, ids, ',')

    response = HttpResponse()
    response.content = str(returnValue).strip(',')
    return response

@LoginAuthorize
def GrantRevokePermissionScopeTargets(request):
    try:
        resourceCategory = request.POST['resourceCategory']
        resourceId = request.POST['resourceId']
        targetCategory = request.POST['targetCategory']
        grantTargetIds = request.POST['grantTargetIds']
        revokeTargetIds = request.POST['revokeTargetIds']
    except:
        resourceCategory = None
        resourceId = None
        targetCategory = None
        grantTargetIds = None
        revokeTargetIds = None

    response = HttpResponse()

    permissionItemId = PermissionItemService.GetEntityByCode(None, "Resource.ManagePermission").id

    if not resourceId:
        response.content = json.dumps({'Success': True, 'Data': '0', 'Message': '请选择相应的资源！'})
        return response

    successFlag = 0
    if str(grantTargetIds).strip(',') and grantTargetIds and (grantTargetIds != ','):
        arrayGrantIds = str(grantTargetIds).strip(',').split(',')
        successFlag = successFlag + ResourcePermission.GrantPermissionScopeTarget(None, resourceCategory, resourceId, targetCategory, arrayGrantIds, permissionItemId)

    if str(revokeTargetIds).strip(','):
        arrayRevokeIds = str(revokeTargetIds).strip(',').split(',')

        def not_empty(s):
            return s and s.strip()

        arrayRevokeIds = list(filter(not_empty, arrayRevokeIds))
        successFlag = successFlag + ResourcePermission.RevokePermissionScopeTarget(None, resourceCategory, resourceId, targetCategory, arrayRevokeIds, permissionItemId)

    if successFlag > 0:
        successFlag = 1
        response.content = json.dumps({'Success': True, 'Data': successFlag, 'Message': '操作成功！'})
        return response
    else:
        response.content = json.dumps({'Success': True, 'Data': successFlag, 'Message': '操作失败！'})
        return response
