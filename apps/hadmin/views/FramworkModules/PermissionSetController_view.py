# _*_ coding: utf-8 _*_
__author__ = 'baxuelong@163.com'
__date__ = '2019/1/22 8:02'

from apps.hadmin.MvcAppUtilties.LoginAuthorize import LoginAuthorize
from django.http.response import HttpResponse
from apps.hadmin.MvcAppUtilties.AjaxOnly import AjaxOnly
from django.template import loader ,Context
from apps.hadmin.MvcAppUtilties.CommonUtils import CommonUtils
from apps.bizlogic.service.permission.ResourcePermission import ResourcePermission
from apps.bizlogic.service.permission.RolePermission import RolePermission
from apps.bizlogic.service.base.PermissionItemService import PermissionItemService
from apps.bizlogic.service.permission.UserPermission import UserPermission
from apps.bizlogic.service.base.UserRoleService import UserRoleService
from apps.bizlogic.service.permission.ModulePermission import ModulePermission
from apps.bizlogic.service.base.RoleService import RoleService
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
def RolePermissionSet(request):
    response = HttpResponse()
    tmp = loader.get_template('PermissionSet/RolePermissionSet.html')  # 加载模板
    render_content = {}  # 将要渲染到模板的数据
    new_body = tmp.render(render_content)  # 渲染模板
    response.content = new_body  # 设置返回内容
    return response

@LoginAuthorize
def RoleUserBatchSet(request):
    response = HttpResponse()
    tmp = loader.get_template('PermissionSet/RoleUserBatchSet.html')  # 加载模板
    render_content = {}  # 将要渲染到模板的数据
    new_body = tmp.render(render_content)  # 渲染模板
    response.content = new_body  # 设置返回内容
    return response


@LoginAuthorize
def UserPermissionSet(request):
    response = HttpResponse()
    tmp = loader.get_template('PermissionSet/UserPermissionSet.html')  # 加载模板
    render_content = {}  # 将要渲染到模板的数据
    new_body = tmp.render(render_content)  # 渲染模板
    response.content = new_body  # 设置返回内容
    return response


@LoginAuthorize
def UserRoleSet(request):
    response = HttpResponse()
    tmp = loader.get_template('PermissionSet/UserRoleSet.html')  # 加载模板
    render_content = {}  # 将要渲染到模板的数据
    new_body = tmp.render(render_content)  # 渲染模板
    response.content = new_body  # 设置返回内容
    return response

def UserPermissionBatchSet(request):
    response = HttpResponse()
    tmp = loader.get_template('PermissionSet/UserPermissionBatchSet.html')  # 加载模板
    render_content = {}  # 将要渲染到模板的数据
    new_body = tmp.render(render_content)  # 渲染模板
    response.content = new_body  # 设置返回内容
    return response

@LoginAuthorize
def UserRoleBatchSet(request):
    response = HttpResponse()
    tmp = loader.get_template('PermissionSet/UserRoleBatchSet.html')  # 加载模板
    render_content = {}  # 将要渲染到模板的数据
    new_body = tmp.render(render_content)  # 渲染模板
    response.content = new_body  # 设置返回内容
    return response


@LoginAuthorize
def RolePermissionBatchSet(request):
    response = HttpResponse()
    tmp = loader.get_template('PermissionSet/RolePermissionBatchSet.html')  # 加载模板
    render_content = {}  # 将要渲染到模板的数据
    new_body = tmp.render(render_content)  # 渲染模板
    response.content = new_body  # 设置返回内容
    return response


@LoginAuthorize
def PermissionScopForm(request):
    response = HttpResponse()
    tmp = loader.get_template('PermissionSet/PermissionScopForm.html')  # 加载模板
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

@LoginAuthorize
def GetModuleByRoleId(request):
    try:
        roleId = request.POST['roleId']
    except:
        roleId = None

    if roleId:
        moduleIds = RolePermission.GetScopeModuleIdsByRoleId(None, roleId, "Resource.AccessPermission")
        returnValue = StringHelper.GetSpitString(moduleIds, ',')
        response = HttpResponse()
        response.content = returnValue
        return response
    else:
        response = HttpResponse()
        response.content = ''
        return response

@LoginAuthorize
def GetPermissionItemsByRoleId(request):
    try:
        roleId = request.POST['roleId']
    except:
        roleId = None

    if roleId:
        ids = RolePermission.GetRolePermissionItemIds(None, roleId)
        returnValue = StringHelper.GetSpitString(ids, ',')
        response = HttpResponse()
        response.content = returnValue
        return response
    else:
        response = HttpResponse()
        response.content = ''
        return response

@LoginAuthorize
def SetRoleModulePermission(request):

    try:
        roleId = request.POST['roleId']
    except:
        roleId = None

    try:
        grantIds = request.POST['grantIds']
    except:
        grantIds = None

    try:
        revokeIds = request.POST['revokeIds']
    except:
        revokeIds = None

    response = HttpResponse()
    vUser = CommonUtils.Current(response, request)

    if not roleId:
        response.content = json.dumps({'Success': False, 'Data': '0', 'Message': '请选择相应的角色！'})
        return response

    successFlag = 0

    if grantIds and (grantIds != ','):
        arrayGrantIds = str(grantIds).strip(',').split(',')
        if len(arrayGrantIds) > 0:
            successFlag = successFlag + RolePermission.GrantRoleModuleScope(vUser, roleId, "Resource.AccessPermission", arrayGrantIds)
        else:
            successFlag = 1

    if revokeIds and (revokeIds != ','):
        arrayRevokeIds = str(revokeIds).strip(',').split(',')
        if len(arrayRevokeIds) > 0:
            successFlag = successFlag + RolePermission.RevokeRoleModuleScope(None, roleId, "Resource.AccessPermission", arrayRevokeIds)
        else:
            successFlag = 1

    if successFlag > 0:
        successFlag = 1
        response.content = json.dumps({'Success': True, 'Data': '1', 'Message': '操作成功！'})
        return response
    else:
        response.content = json.dumps({'Success': False, 'Data': '0', 'Message': '操作失败！'})
        return response


@LoginAuthorize
def SetRolePermissionItem(request):
    try:
        roleId = request.POST['roleId']
    except:
        roleId = None

    try:
        grantIds = request.POST['grantIds']
    except:
        grantIds = None

    try:
        revokeIds = request.POST['revokeIds']
    except:
        revokeIds = None

    response = HttpResponse()
    vUser = CommonUtils.Current(response, request)

    if not roleId:
        response.content = json.dumps({'Success': False, 'Data': '0', 'Message': '请选择相应的角色！'})
        return response

    successFlag = 0

    if grantIds and (grantIds != ','):
        arrayGrantIds = str(grantIds).strip(',').split(',')
        if len(arrayGrantIds) > 0:
            successFlag = successFlag + RolePermission.GrantRolePermissions(vUser, [roleId], arrayGrantIds)
        else:
            successFlag = 1

    if revokeIds and (revokeIds != ','):
        arrayRevokeIds = str(revokeIds).strip(',').split(',')
        if len(arrayRevokeIds) > 0:
            successFlag = successFlag + RolePermission.RevokeRolePermissions(None, [roleId], arrayRevokeIds)
        else:
            successFlag = 1

    if successFlag > 0:
        successFlag = 1
        response.content = json.dumps({'Success': True, 'Data': '1', 'Message': '操作成功！'})
        return response
    else:
        response.content = json.dumps({'Success': False, 'Data': '0', 'Message': '操作失败！'})
        return response

@LoginAuthorize
def GetModuleByUserId(request):
    try:
        userId = request.POST['userId']
    except:
        userId = None

    if userId:
        moduleIds = UserPermission.GetScopeModuleIdsByUserId(None, userId, "Resource.AccessPermission")
        returnValue = StringHelper.GetSpitString(moduleIds, ',')
        response = HttpResponse()
        response.content = returnValue
        return response
    else:
        response = HttpResponse()
        response.content = ''
        return response

@LoginAuthorize
def SetUserModulePermission(request):
    try:
        userId = request.POST['userId']
    except:
        userId = None

    try:
        grantIds = request.POST['grantIds']
    except:
        grantIds = None

    try:
        revokeIds = request.POST['revokeIds']
    except:
        revokeIds = None

    response = HttpResponse()
    vUser = CommonUtils.Current(response, request)

    if not userId:
        response.content = json.dumps({'Success': False, 'Data': '0', 'Message': '请选择相应的用户！'})
        return response

    successFlag = 0

    if grantIds and (grantIds != ','):
        arrayGrantIds = str(grantIds).strip(',').split(',')
        if len(arrayGrantIds) > 0:
            successFlag = successFlag + UserPermission.GrantUserModuleScope(CommonUtils.Current(response, request), userId, "Resource.AccessPermission", arrayGrantIds)
        else:
            successFlag = 1

    if revokeIds and (revokeIds != ','):
        arrayRevokeIds = str(revokeIds).strip(',').split(',')
        if len(arrayRevokeIds) > 0:
            successFlag = successFlag + UserPermission.RevokeUserModuleScope(None, userId, "Resource.AccessPermission", arrayRevokeIds)
        else:
            successFlag = 1

    if successFlag > 0:
        successFlag = 1
        response.content = json.dumps({'Success': True, 'Data': '1', 'Message': '操作成功！'})
        return response
    else:
        response.content = json.dumps({'Success': False, 'Data': '0', 'Message': '操作失败！'})
        return response


@LoginAuthorize
def GetPermissionItemsByUserId(request):
    try:
        userId = request.POST['userId']
    except:
        userId = None

    if userId:
        ids = UserPermission.GetUserPermissionItemIds(None, userId)
        returnValue = StringHelper.GetSpitString(ids, ',')
        response = HttpResponse()
        response.content = returnValue
        return response
    else:
        response = HttpResponse()
        response.content = ''
        return response


@LoginAuthorize
def SetUserPermissionItem(request):
    try:
        userId = request.POST['userId']
    except:
        userId = None

    try:
        grantIds = request.POST['grantIds']
    except:
        grantIds = None

    try:
        revokeIds = request.POST['revokeIds']
    except:
        revokeIds = None

    response = HttpResponse()
    vUser = CommonUtils.Current(response, request)

    if not userId:
        response.content = json.dumps({'Success': False, 'Data': '0', 'Message': '请选择相应的用户！'})
        return response

    successFlag = 0

    if grantIds and (grantIds != ','):
        arrayGrantIds = str(grantIds).strip(',').split(',')
        if len(arrayGrantIds) > 0:
            successFlag = successFlag + UserPermission.GrantUserPermissions(CommonUtils.Current(response, request), [userId], arrayGrantIds)
        else:
            successFlag = 1

    if revokeIds and (revokeIds != ','):
        arrayRevokeIds = str(revokeIds).strip(',').split(',')
        if len(arrayRevokeIds) > 0:
            successFlag = successFlag + UserPermission.RevokeUserPermissions(None, [userId], arrayRevokeIds)
        else:
            successFlag = 1

    if successFlag > 0:
        successFlag = 1
        response.content = json.dumps({'Success': True, 'Data': '1', 'Message': '操作成功！'})
        return response
    else:
        response.content = json.dumps({'Success': False, 'Data': '0', 'Message': '操作失败！'})
        return response

@LoginAuthorize
def GetUserRoleIds(request):
    try:
        userId = request.POST['userId']
    except:
        userId = None

    if userId:
        ids = UserRoleService.GetUserRoleIds(None, userId)
        returnValue = StringHelper.GetSpitString(ids, ',')
        response = HttpResponse()
        response.content = returnValue
        return response
    else:
        response = HttpResponse()
        response.content = ''
        return response

@LoginAuthorize
def AddUserToRole(request):
    try:
        userId = request.POST['userId']
    except:
        userId = None

    try:
        targetIds = request.POST['targetIds']
    except:
        targetIds = None
    response = HttpResponse()
    returnValue = UserRoleService.AddUserToRole(CommonUtils.Current(response, request), userId, targetIds)
    if returnValue:
        response.content = json.dumps({'Success': True, 'Data': '1', 'Message': '添加成功！'})
        return response
    else:
        response.content = json.dumps({'Success': False, 'Data': '0', 'Message': '添加失败！'})
        return response

@LoginAuthorize
def RemoveUserFromRole(request):
    try:
        userId = request.POST['userId']
    except:
        roleId = None

    try:
        targetIds = request.POST['targetIds']
    except:
        targetIds = None
    response = HttpResponse()
    returnValue = UserRoleService.RemoveUserFromRole(None, userId, targetIds)
    if returnValue > 0:
        successFlag = 1
        response.content = json.dumps({'Success': True, 'Data': '1', 'Message': '操作成功！'})
        return response
    else:
        response.content = json.dumps({'Success': False, 'Data': '0', 'Message': '操作失败！'})
        return response

@LoginAuthorize
def PermissionScopForm(request):
    response = HttpResponse()
    tmp = loader.get_template('PermissionSet/PermissionScopForm.html')  # 加载模板
    render_content = {}  # 将要渲染到模板的数据
    new_body = tmp.render(render_content)  # 渲染模板
    response.content = new_body  # 设置返回内容
    return response

@LoginAuthorize
def GetRoleUserIds(request):
    try:
        roleId = request.POST['roleId']
    except:
        roleId = None

    dtScope = RoleService.GetRoleUserIds(None, roleId)

    returnValue = StringHelper.GetSpitString(dtScope, ',')

    response = HttpResponse()
    response.content = returnValue
    return response

@LoginAuthorize
def AddRoleUser(request):
    try:
        roleId = request.POST['roleId']
    except:
        userId = None
    try:
        targetIds = request.POST['targetIds']
    except:
        targetIds = None
    returnValue = 0
    response = HttpResponse()
    for id in str(targetIds).split(','):
        UserRoleService.AddUserToRole(CommonUtils.Current(response, request), id, roleId)
        returnValue = returnValue + 1

    if returnValue > 0:
        response.content = json.dumps({'Success': True, 'Data': '1', 'Message': '添加成功！'})
        return response
    else:
        response.content = json.dumps({'Success': False, 'Data': '0', 'Message': '添加失败！'})
        return response

@LoginAuthorize
def RemoveRoleUser(request):
    try:
        roleId = request.POST['roleId']
    except:
        roleId = None

    try:
        targetIds = request.POST['targetIds']
    except:
        targetIds = None
    response = HttpResponse()
    for id in str(targetIds).split(','):
        returnValue = UserRoleService.RemoveUserFromRole(None, id, roleId)
    if returnValue > 0:
        successFlag = 1
        response.content = json.dumps({'Success': True, 'Data': '1', 'Message': '操作成功！'})
        return response
    else:
        response.content = json.dumps({'Success': False, 'Data': '0', 'Message': '操作失败！'})
        return response