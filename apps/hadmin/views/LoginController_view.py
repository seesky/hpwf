# _*_ coding: utf-8 _*_
__author__ = 'baxuelong@163.com'
__date__ = '2019/1/4 11:05'

from django.shortcuts import render
from django.http import HttpResponse
from django.core.cache import cache

from apps.utilities.publiclibrary.NetHelper import NetHelper
from apps.utilities.publiclibrary.SystemInfo import SystemInfo
from apps.utilities.publiclibrary.UserInfo import UserInfo
from apps.hadmin.MvcAppUtilties.CommonUtils import CommonUtils
from apps.bizlogic.service.base.LogOnService import LogOnService
from apps.utilities.message.StatusCode import StatusCode


def Index(request):
    return render(request, 'Login/Index.html')

def CheckLogin(request):
    if request.method == 'GET':
        return render(request, 'Login/Index.html')
    else:
        Msg = ''
        IPAddress = NetHelper.GetIpAddress(request)
        Account = ''
        Password = ''
        Token = ''
        try:
            Account = request.POST['Account']
            Password = request.POST['Password']

            if Account == SystemInfo.CurrentUserName:
                if Password == SystemInfo.CurrentPassword:
                    imanageuser = UserInfo()
                    imanageuser.Id = 'Administrator'
                    imanageuser.UserName = '超级管理员'
                    imanageuser.Code = 'Administrator'
                    imanageuser.CompanyId = '系统'
                    imanageuser.DepartmentId = '系统'
                    imanageuser.IPAddress = IPAddress
                    imanageuser.IsAdministrator = True
                    #TODO:需要做在线人数统计

                    Msg = '3'
                    response = HttpResponse(Msg)
                    CommonUtils.AddCurrent(imanageuser, response, request)
                    response.set_cookie('UIStyle', CommonUtils.UIStyle(imanageuser, response, request))
                    return response
                else:
                    Msg = '4'
                    return HttpResponse(Msg)
            else:


                returnStatusCode = ''

                returnStatusCode,userInfo = LogOnService.UserLogOn(Account, Password, '', False, IPAddress)

                if returnStatusCode == StatusCode.statusCodeDic.get('OK'):
                    Msg = '3'
                    response = HttpResponse(Msg)
                    CommonUtils.AddCurrent(userInfo, response, request)
                    response.set_cookie('UIStyle', CommonUtils.UIStyle(userInfo, response, request))
                    return response
                else:
                    Msg = '4'

        except Exception as e:
            print(e)

        return HttpResponse(Msg)

def OutLogin(request):
    response = HttpResponse()
    LogOnService.OnExit(None, CommonUtils.Current(response, request).Id)
    CommonUtils.EmptyCurrent(response, request)
    request.session.flush()
    response.content = '1'
    return response