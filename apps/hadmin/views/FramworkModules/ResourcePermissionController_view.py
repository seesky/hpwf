# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2019/1/25 13:50'

from apps.bizlogic.service.permission.UserPermission import UserPermission
from apps.bizlogic.service.permission.RolePermission import RolePermission
from apps.utilities.publiclibrary.StringHelper import StringHelper
from django.http.response import HttpResponse
import json
from apps.hadmin.MvcAppUtilties.CommonUtils import CommonUtils
from apps.hadmin.MvcAppUtilties.LoginAuthorize import LoginAuthorize

@LoginAuthorize
def GetScopeUserIdsByUserId(request):
    try:
        userId = request.POST['userId']
    except:
        userId = None
    if userId:
        userIds = UserPermission.GetScopeUserIdsByUserId(None, userId, "Resource.ManagePermission")
        returnValue = '['
        for id in userIds:
            returnValue = returnValue + '"' + id + '",'
        returnValue = returnValue.strip(',')
        returnValue = returnValue + ']'
        response = HttpResponse()
        response.content = returnValue
        return response
    else:
        response = HttpResponse()
        response.content = '[]'
        return response

@LoginAuthorize
def GetScopeRoleIdsByUserId(request):
    try:
        userId = request.POST['userId']
    except:
        userId = None
    if userId:
        roleIds = UserPermission.GetScopeRoleIdsByUserId(None, userId, "Resource.ManagePermission")
        returnValue = '['
        for id in roleIds:
            returnValue = returnValue + '"' + id + '",'
        returnValue = returnValue.strip(',')
        returnValue = returnValue + ']'
        response = HttpResponse()
        response.content = returnValue
        return response
    else:
        response = HttpResponse()
        response.content = '[]'
        return response


@LoginAuthorize
def GetScopeModuleIdsByUserId(request):
    try:
        userId = request.POST['userId']
    except:
        userId = None
    if userId:
        moduleIds = UserPermission.GetScopeModuleIdsByUserId(None, userId, "Resource.ManagePermission")
        returnValue = '['
        for id in moduleIds:
            returnValue = returnValue + '"' + id + '",'
        returnValue = returnValue.strip(',')
        returnValue = returnValue + ']'
        response = HttpResponse()
        response.content = returnValue
        return response
    else:
        response = HttpResponse()
        response.content = '[]'
        return response

@LoginAuthorize
def GetScopePermissionItemIdsByUserId(request):
    try:
        userId = request.POST['userId']
    except:
        userId = None
    if userId:
        scopeIds = UserPermission.GetScopePermissionItemIdsByUserId(None, userId, "Resource.ManagePermission")
        returnValue = '['
        for id in scopeIds:
            returnValue = returnValue + '"' + id + '",'
        returnValue = returnValue.strip(',')
        returnValue = returnValue + ']'
        response = HttpResponse()
        response.content = returnValue
        return response
    else:
        response = HttpResponse()
        response.content = '[]'
        return response

@LoginAuthorize
def GetScopeRoleIdsByRoleId(request):
    try:
        roleId = request.POST['roleId']
    except:
        roleId = None
    if roleId:
        scopeIds = RolePermission.GetScopeRoleIdsByRoleId(None, roleId, "Resource.ManagePermission")
        returnValue = '['
        for id in scopeIds:
            returnValue = returnValue + '"' + id + '",'
        returnValue = returnValue.strip(',')
        returnValue = returnValue + ']'
        response = HttpResponse()
        response.content = returnValue
        return response
    else:
        response = HttpResponse()
        response.content = '[]'
        return response

@LoginAuthorize
def GetScopeUserIdsByRoleId(request):
    try:
        roleId = request.POST['roleId']
    except:
        roleId = None
    if roleId:
        scopeIds = RolePermission.GetScopeUserIdsByRoleId(None, roleId, "Resource.ManagePermission")
        returnValue = '['
        for id in scopeIds:
            returnValue = returnValue + '"' + id + '",'
        returnValue = returnValue.strip(',')
        returnValue = returnValue + ']'
        response = HttpResponse()
        response.content = returnValue
        return response
    else:
        response = HttpResponse()
        response.content = '[]'
        return response

@LoginAuthorize
def GetScopeOrganizeIdsByRoleId(request):
    try:
        roleId = request.POST['roleId']
    except:
        roleId = None
    if roleId:
        scopeIds = RolePermission.GetScopeOrganizeIdsByRoleId(None, roleId, "Resource.ManagePermission")
        returnValue = '['
        for id in scopeIds:
            returnValue = returnValue + '"' + id + '",'
        returnValue = returnValue.strip(',')
        returnValue = returnValue + ']'
        response = HttpResponse()
        response.content = returnValue
        return response
    else:
        response = HttpResponse()
        response.content = '[]'
        return response

@LoginAuthorize
def GetScopeModuleIdsByRoleId(request):
    try:
        roleId = request.POST['roleId']
    except:
        roleId = None
    if roleId:
        scopeIds = RolePermission.GetScopeModuleIdsByRoleId(None, roleId, "Resource.ManagePermission")
        returnValue = '['
        for id in scopeIds:
            returnValue = returnValue + '"' + id + '",'
        returnValue = returnValue.strip(',')
        returnValue = returnValue + ']'
        response = HttpResponse()
        response.content = returnValue
        return response
    else:
        response = HttpResponse()
        response.content = '[]'
        return response

@LoginAuthorize
def GetScopePermissionItemIdsByRoleId(request):
    try:
        roleId = request.POST['roleId']
    except:
        roleId = None
    if roleId:
        scopeIds = RolePermission.GetScopePermissionItemIdsByRoleId(None, roleId, "Resource.ManagePermission")
        returnValue = '['
        for id in scopeIds:
            returnValue = returnValue + '"' + id + '",'
        returnValue = returnValue.strip(',')
        returnValue = returnValue + ']'
        response = HttpResponse()
        response.content = returnValue
        return response
    else:
        response = HttpResponse()
        response.content = '[]'
        return response

@LoginAuthorize
def GetScopeOrganizeIdsByUserId(request):
    try:
        userId = request.POST['userId']
    except:
        userId = None
    if userId:
        orgIds = UserPermission.GetScopeOrganizeIdsByUserId(None, userId, "Resource.ManagePermission")
        returnValue = '['
        for id in orgIds:
            returnValue = returnValue + '"' + id + '",'
        returnValue = returnValue.strip(',')
        returnValue = returnValue + ']'
        response = HttpResponse()
        response.content = returnValue
        return response
    else:
        response = HttpResponse()
        response.content = '[]'
        return response

@LoginAuthorize
def SaveUserUserScope(request):
    try:
        targetUserId = request.POST['targetUserId']
    except:
        targetUserId = None

    try:
        userIds = request.POST['userIds']
    except:
        userIds = None

    response = HttpResponse()

    if not targetUserId:
        response.content = json.dumps({'Success': True, 'Data': '-1', 'Message': '用户主键为空！'})
        return response
    try:
        tmpUserids = UserPermission.GetScopeUserIdsByUserId(None, targetUserId, "Resource.ManagePermission")

        if not userIds:
            if tmpUserids and len(tmpUserids) > 0:
                UserPermission.RevokeUserUserScope(None, targetUserId, "Resource.ManagePermission", tmpUserids)
        else:
            # revokeIds = list(set(tmpRoleIds) ^ set(str(roleIds).split(',')))
            revokeIds = []
            for r in tmpUserids:
                if r not in userIds:
                    revokeIds.append(r)

            # grantIds = list(set(str(roleIds).split(',')) ^ set(tmpRoleIds))
            grantIds = []
            for g in str(userIds).split(','):
                if g not in tmpUserids:
                    grantIds.append(g)
            if len(grantIds) > 0:
                UserPermission.GrantUserUserScope(None, targetUserId, "Resource.ManagePermission", grantIds)

            if len(revokeIds) > 0:
                UserPermission.RevokeUserUserScope(None, targetUserId, "Resource.ManagePermission", revokeIds)
        response.content = json.dumps({'Success': True, 'Data': '1', 'Message': "授权成功！"})
        return response
    except:
        response.content = json.dumps({'Success': False, 'Data': '-2', 'Message': '操作失败！'})
        return response

@LoginAuthorize
def SaveUserRoleScope(request):
    try:
        targetUserId = request.POST['targetUserId']
    except:
        targetUserId = None

    try:
        roleIds = request.POST['roleIds']
    except:
        roleIds = None

    response = HttpResponse()

    if not targetUserId:
        response.content = json.dumps({'Success': True, 'Data': '-1', 'Message': '用户主键为空！'})
        return response

    try:
        tmpRoleIds = UserPermission.GetScopeRoleIdsByUserId(None, targetUserId, "Resource.ManagePermission")

        if not roleIds:
            if tmpRoleIds and len(tmpRoleIds) > 0:
                UserPermission.RevokeUserRoleScope(None, targetUserId, "Resource.ManagePermission", tmpRoleIds)
        else:

            #revokeIds = list(set(tmpRoleIds) ^ set(str(roleIds).split(',')))
            revokeIds = []
            for r in tmpRoleIds:
                if r not in roleIds:
                    revokeIds.append(r)

            #grantIds = list(set(str(roleIds).split(',')) ^ set(tmpRoleIds))
            grantIds = []
            for g in str(roleIds).split(','):
                if g not in tmpRoleIds:
                    grantIds.append(g)

            if len(grantIds) > 0:
                UserPermission.GrantUserRoleScope(None, targetUserId, "Resource.ManagePermission", grantIds)

            if len(revokeIds) > 0:
                UserPermission.RevokeUserRoleScope(None, targetUserId, "Resource.ManagePermission", revokeIds)
        response.content = json.dumps({'Success': True, 'Data': '1', 'Message': "授权成功！"})
        return response
    except:
        response.content = json.dumps({'Success': False, 'Data': '-2', 'Message': '操作失败！'})
        return response

@LoginAuthorize
def SaveOrganizeScope(request):
    try:
        targetUserId = request.POST['targetUserId']
    except:
        targetUserId = None

    try:
        organizeIds = request.POST['organizeIds']
    except:
        organizeIds = None

    response = HttpResponse()

    if not targetUserId:
        response.content = json.dumps({'Success': True, 'Data': '-1', 'Message': '用户主键为空！'})
        return response

    try:
        tmpOrgIds = UserPermission.GetScopeOrganizeIdsByUserId(None, targetUserId, "Resource.ManagePermission")

        if not organizeIds:
            if tmpOrgIds and len(tmpOrgIds) > 0:
                UserPermission.RevokeUserOrganizeScope(None, targetUserId, "Resource.ManagePermission", tmpOrgIds)
        else:

            #revokeIds = list(set(tmpRoleIds) ^ set(str(roleIds).split(',')))
            revokeIds = []
            for r in tmpOrgIds:
                if r not in organizeIds:
                    revokeIds.append(r)

            #grantIds = list(set(str(roleIds).split(',')) ^ set(tmpRoleIds))
            grantIds = []
            for g in str(organizeIds).split(','):
                if g not in tmpOrgIds:
                    grantIds.append(g)

            if len(grantIds) > 0:
                UserPermission.GrantUserOrganizeScope(None, targetUserId, "Resource.ManagePermission", grantIds)

            if len(revokeIds) > 0:
                UserPermission.RevokeUserOrganizeScope(None, targetUserId, "Resource.ManagePermission", revokeIds)
        response.content = json.dumps({'Success': True, 'Data': '1', 'Message': "授权成功！"})
        return response
    except:
        response.content = json.dumps({'Success': False, 'Data': '-2', 'Message': '操作失败！'})
        return response

@LoginAuthorize
def SaveModuleScope(request):
    try:
        targetUserId = request.POST['targetUserId']
    except:
        targetUserId = None

    try:
        moduleIds = request.POST['moduleIds']
    except:
        moduleIds = None

    response = HttpResponse()

    if not targetUserId:
        response.content = json.dumps({'Success': True, 'Data': '-1', 'Message': '用户主键为空！'})
        return response

    try:
        tmpModuleIds = UserPermission.GetScopeModuleIdsByUserId(None, targetUserId, "Resource.ManagePermission")

        if not moduleIds:
            if tmpModuleIds and len(tmpModuleIds) > 0:
                UserPermission.RevokeUserModuleScope(None, targetUserId, "Resource.ManagePermission", tmpModuleIds)
        else:

            #revokeIds = list(set(tmpRoleIds) ^ set(str(roleIds).split(',')))
            revokeIds = []
            for r in tmpModuleIds:
                if r not in moduleIds:
                    revokeIds.append(r)

            #grantIds = list(set(str(roleIds).split(',')) ^ set(tmpRoleIds))
            grantIds = []
            for g in str(moduleIds).split(','):
                if g not in tmpModuleIds:
                    grantIds.append(g)

            if len(grantIds) > 0:
                UserPermission.GrantUserModuleScope(CommonUtils.Current(response, request), targetUserId, "Resource.ManagePermission", grantIds)

            if len(revokeIds) > 0:
                UserPermission.RevokeUserModuleScope(None, targetUserId, "Resource.ManagePermission", revokeIds)
        response.content = json.dumps({'Success': True, 'Data': '1', 'Message': "授权成功！"})
        return response
    except:
        response.content = json.dumps({'Success': False, 'Data': '-2', 'Message': '操作失败！'})
        return response

@LoginAuthorize
def SavePermissionItemScope(request):
    try:
        targetUserId = request.POST['targetUserId']
    except:
        targetUserId = None

    try:
        permissionItemIds = request.POST['permissionItemIds']
    except:
        permissionItemIds = None

    response = HttpResponse()

    if not targetUserId:
        response.content = json.dumps({'Success': True, 'Data': '-1', 'Message': '用户主键为空！'})
        return response

    try:
        tmpScopeIds = UserPermission.GetScopePermissionItemIdsByUserId(None, targetUserId, "Resource.ManagePermission")

        if not permissionItemIds:
            if tmpScopeIds and len(tmpScopeIds) > 0:
                UserPermission.RevokeUserPermissionItemScope(None, targetUserId, "Resource.ManagePermission", tmpScopeIds)
        else:

            #revokeIds = list(set(tmpRoleIds) ^ set(str(roleIds).split(',')))
            revokeIds = []
            for r in tmpScopeIds:
                if r not in permissionItemIds:
                    revokeIds.append(r)

            #grantIds = list(set(str(roleIds).split(',')) ^ set(tmpRoleIds))
            grantIds = []
            for g in str(permissionItemIds).split(','):
                if g not in tmpScopeIds:
                    grantIds.append(g)

            if len(grantIds) > 0:
                UserPermission.GrantUserPermissionItemScope(CommonUtils.Current(response, request), targetUserId, "Resource.ManagePermission", grantIds)

            if len(revokeIds) > 0:
                UserPermission.RevokeUserPermissionItemScope(None, targetUserId, "Resource.ManagePermission", revokeIds)
        response.content = json.dumps({'Success': True, 'Data': '1', 'Message': "授权成功！"})
        return response
    except:
        response.content = json.dumps({'Success': False, 'Data': '-2', 'Message': '操作失败！'})
        return response

@LoginAuthorize
def SaveRoleUserScope(request):
    try:
        targetRoleId = request.POST['targetRoleId']
    except:
        targetRoleId = None

    try:
        userIds = request.POST['userIds']
    except:
        userIds = None

    response = HttpResponse()

    if not targetRoleId:
        response.content = json.dumps({'Success': True, 'Data': '-1', 'Message': '角色主键为空！'})
        return response

    try:
        tmpUserIds = RolePermission.GetScopeUserIdsByRoleId(None, targetRoleId, "Resource.ManagePermission")

        if not userIds:
            if tmpUserIds and len(tmpUserIds) > 0:
                RolePermission.RevokeRoleUserScope(None, targetRoleId, "Resource.ManagePermission", tmpUserIds)
        else:

            #revokeIds = list(set(tmpRoleIds) ^ set(str(roleIds).split(',')))
            revokeIds = []
            for r in tmpUserIds:
                if r not in userIds:
                    revokeIds.append(r)

            #grantIds = list(set(str(roleIds).split(',')) ^ set(tmpRoleIds))
            grantIds = []
            for g in str(userIds).split(','):
                if g not in tmpUserIds:
                    grantIds.append(g)

            if len(grantIds) > 0:
                RolePermission.GrantRoleUserScope(CommonUtils.Current(response, request), targetRoleId, "Resource.ManagePermission", grantIds)

            if len(revokeIds) > 0:
                RolePermission.RevokeRoleUserScope(None, targetRoleId, "Resource.ManagePermission", revokeIds)
        response.content = json.dumps({'Success': True, 'Data': '1', 'Message': "授权成功！"})
        return response
    except:
        response.content = json.dumps({'Success': False, 'Data': '-2', 'Message': '操作失败！'})
        return response


@LoginAuthorize
def SaveRoleRoleScope(request):
    try:
        targetRoleId = request.POST['targetRoleId']
    except:
        targetRoleId = None

    try:
        roleIds = request.POST['roleIds']
    except:
        roleIds = None

    response = HttpResponse()

    if not targetRoleId:
        response.content = json.dumps({'Success': True, 'Data': '-1', 'Message': '角色主键为空！'})
        return response

    try:
        tmpRoleIds = RolePermission.GetScopeRoleIdsByRoleId(None, targetRoleId, "Resource.ManagePermission")

        if not roleIds:
            if tmpRoleIds and len(tmpRoleIds) > 0:
                RolePermission.RevokeRoleRoleScope(None, targetRoleId, "Resource.ManagePermission", tmpRoleIds)
        else:

            #revokeIds = list(set(tmpRoleIds) ^ set(str(roleIds).split(',')))
            revokeIds = []
            for r in tmpRoleIds:
                if r not in roleIds:
                    revokeIds.append(r)

            #grantIds = list(set(str(roleIds).split(',')) ^ set(tmpRoleIds))
            grantIds = []
            for g in str(roleIds).split(','):
                if g not in tmpRoleIds:
                    grantIds.append(g)

            if len(grantIds) > 0:
                RolePermission.GrantRoleRoleScope(CommonUtils.Current(response, request), targetRoleId, "Resource.ManagePermission", grantIds)

            if len(revokeIds) > 0:
                RolePermission.RevokeRoleRoleScope(None, targetRoleId, "Resource.ManagePermission", revokeIds)
        response.content = json.dumps({'Success': True, 'Data': '1', 'Message': "授权成功！"})
        return response
    except:
        response.content = json.dumps({'Success': False, 'Data': '-2', 'Message': '操作失败！'})
        return response


@LoginAuthorize
def SaveRoleOrganizeScope(request):
    try:
        targetRoleId = request.POST['targetRoleId']
    except:
        targetRoleId = None

    try:
        organizeIds = request.POST['organizeIds']
    except:
        organizeIds = None

    response = HttpResponse()

    if not targetRoleId:
        response.content = json.dumps({'Success': True, 'Data': '-1', 'Message': '角色主键为空！'})
        return response

    try:
        tmpOrgIds = RolePermission.GetScopeOrganizeIdsByRoleId(None, targetRoleId, "Resource.ManagePermission")

        if not organizeIds:
            if tmpOrgIds and len(tmpOrgIds) > 0:
                RolePermission.RevokeRoleOrganizeScope(None, targetRoleId, "Resource.ManagePermission", tmpOrgIds)
        else:

            #revokeIds = list(set(tmpRoleIds) ^ set(str(roleIds).split(',')))
            revokeIds = []
            for r in tmpOrgIds:
                if r not in organizeIds:
                    revokeIds.append(r)

            #grantIds = list(set(str(roleIds).split(',')) ^ set(tmpRoleIds))
            grantIds = []
            for g in str(organizeIds).split(','):
                if g not in tmpOrgIds:
                    grantIds.append(g)

            if len(grantIds) > 0:
                RolePermission.GrantRoleOrganizeScope(CommonUtils.Current(response, request), targetRoleId, "Resource.ManagePermission", grantIds)

            if len(revokeIds) > 0:
                RolePermission.RevokeRoleOrganizeScope(None, targetRoleId, "Resource.ManagePermission", revokeIds)
        response.content = json.dumps({'Success': True, 'Data': '1', 'Message': "授权成功！"})
        return response
    except:
        response.content = json.dumps({'Success': False, 'Data': '-2', 'Message': '操作失败！'})
        return response

@LoginAuthorize
def SaveRoleModuleScope(request):
    try:
        targetRoleId = request.POST['targetRoleId']
    except:
        targetRoleId = None

    try:
        moduleIds = request.POST['moduleIds']
    except:
        moduleIds = None

    response = HttpResponse()

    if not targetRoleId:
        response.content = json.dumps({'Success': True, 'Data': '-1', 'Message': '角色主键为空！'})
        return response

    try:
        tmpModuleIds = RolePermission.GetScopeModuleIdsByRoleId(None, targetRoleId, "Resource.ManagePermission")

        if not moduleIds:
            if tmpModuleIds and len(tmpModuleIds) > 0:
                RolePermission.RevokeRoleModuleScope(None, targetRoleId, "Resource.ManagePermission", tmpModuleIds)
        else:

            #revokeIds = list(set(tmpRoleIds) ^ set(str(roleIds).split(',')))
            revokeIds = []
            for r in tmpModuleIds:
                if r not in moduleIds:
                    revokeIds.append(r)

            #grantIds = list(set(str(roleIds).split(',')) ^ set(tmpRoleIds))
            grantIds = []
            for g in str(moduleIds).split(','):
                if g not in tmpModuleIds:
                    grantIds.append(g)

            if len(grantIds) > 0:
                RolePermission.GrantRoleModuleScope(CommonUtils.Current(response, request), targetRoleId, "Resource.ManagePermission", grantIds)

            if len(revokeIds) > 0:
                RolePermission.RevokeRoleModuleScope(None, targetRoleId, "Resource.ManagePermission", revokeIds)
        response.content = json.dumps({'Success': True, 'Data': '1', 'Message': "授权成功！"})
        return response
    except:
        response.content = json.dumps({'Success': False, 'Data': '-2', 'Message': '操作失败！'})
        return response


@LoginAuthorize
def SaveRolePermissionItemScope(request):
    try:
        targetRoleId = request.POST['targetRoleId']
    except:
        targetRoleId = None

    try:
        permissionItemIds = request.POST['permissionItemIds']
    except:
        permissionItemIds = None

    response = HttpResponse()

    if not targetRoleId:
        response.content = json.dumps({'Success': True, 'Data': '-1', 'Message': '角色主键为空！'})
        return response

    try:
        tmpScopeIds = RolePermission.GetScopePermissionItemIdsByRoleId(None, targetRoleId, "Resource.ManagePermission")

        if not permissionItemIds:
            if tmpScopeIds and len(tmpScopeIds) > 0:
                RolePermission.RevokeRolePermissionItemScope(None, targetRoleId, "Resource.ManagePermission", tmpScopeIds)
        else:

            #revokeIds = list(set(tmpRoleIds) ^ set(str(roleIds).split(',')))
            revokeIds = []
            for r in tmpScopeIds:
                if r not in permissionItemIds:
                    revokeIds.append(r)

            #grantIds = list(set(str(roleIds).split(',')) ^ set(tmpRoleIds))
            grantIds = []
            for g in str(permissionItemIds).split(','):
                if g not in tmpScopeIds:
                    grantIds.append(g)

            if len(grantIds) > 0:
                RolePermission.GrantRolePermissionItemScope(CommonUtils.Current(response, request), targetRoleId, "Resource.ManagePermission", grantIds)

            if len(revokeIds) > 0:
                RolePermission.RevokeRolePermissionItemScope(None, targetRoleId, "Resource.ManagePermission", revokeIds)
        response.content = json.dumps({'Success': True, 'Data': '1', 'Message': "授权成功！"})
        return response
    except Exception as e:
        print(e)
        response.content = json.dumps({'Success': False, 'Data': '-2', 'Message': '操作失败！'})
        return response