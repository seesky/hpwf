# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2019/1/25 13:50'

from apps.bizlogic.service.permission.UserPermission import UserPermission
from apps.utilities.publiclibrary.StringHelper import StringHelper
from django.http.response import HttpResponse
import json

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

def GetScopeRoleIdsByUserId(request):
    try:
        userId = request.POST['userId']
    except:
        userId = None
    if userId:
        userIds = UserPermission.GetScopeRoleIdsByUserId(None, userId, "Resource.ManagePermission")
        returnValue = '['
        returnValue = returnValue + StringHelper.ArrayToList(None, userIds, ',')
        returnValue = returnValue + ']'
        response = HttpResponse()
        response.content = returnValue
        return response
    else:
        response = HttpResponse()
        response.content = '[]'
        return response



def GetScopeModuleIdsByUserId(request):
    try:
        userId = request.POST['userId']
    except:
        userId = None
    if userId:
        userIds = UserPermission.GetScopeModuleIdsByUserId(None, userId, "Resource.ManagePermission")
        returnValue = '['
        returnValue = returnValue + StringHelper.ArrayToList(None, userIds, ',')
        returnValue = returnValue + ']'
        response = HttpResponse()
        response.content = returnValue
        return response
    else:
        response = HttpResponse()
        response.content = '[]'
        return response

def GetScopePermissionItemIdsByUserId(request):
    try:
        userId = request.POST['userId']
    except:
        userId = None
    if userId:
        userIds = UserPermission.GetScopePermissionItemIdsByUserId(None, userId, "Resource.ManagePermission")
        returnValue = '['
        returnValue = returnValue + StringHelper.ArrayToList(None, userIds, ',')
        returnValue = returnValue + ']'
        response = HttpResponse()
        response.content = returnValue
        return response
    else:
        response = HttpResponse()
        response.content = '[]'
        return response

def GetScopeOrganizeIdsByUserId(request):
    try:
        userId = request.POST['userId']
    except:
        userId = None
    if userId:
        userIds = UserPermission.GetScopeOrganizeIdsByUserId(None, userId, "Resource.ManagePermission")
        returnValue = '['
        returnValue = returnValue + StringHelper.ArrayToList(None, userIds, ',')
        returnValue = returnValue + ']'
        response = HttpResponse()
        response.content = returnValue
        return response
    else:
        response = HttpResponse()
        response.content = '[]'
        return response

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
            if len(tmpUserids) < 0:
                revokeIds = list(set(tmpUserids) ^ set(str(userIds).split(',')))
            else:
                revokeIds = []

            if len(userIds) < 0:
                grantIds = []

            else:
                grantIds = list(set(str(userIds).split(',')) ^ set(tmpUserids))

            if len(grantIds) > 0:
                UserPermission.GrantUserUserScope(None, targetUserId, "Resource.ManagePermission", grantIds)

            if len(revokeIds) > 0:
                UserPermission.RevokeUserUserScope(None, targetUserId, "Resource.ManagePermission", revokeIds)
        response.content = json.dumps({'Success': True, 'Data': '1', 'Message': "授权成功！"})
        return response
    except:
        response.content = json.dumps({'Success': False, 'Data': '-2', 'Message': '操作失败！'})
        return response