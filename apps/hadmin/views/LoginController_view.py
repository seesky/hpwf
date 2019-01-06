# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2019/1/4 11:05'

from django.shortcuts import render
from django.http import HttpResponse
from django.core.cache import cache

from apps.utilities.publiclibrary.NetHelper import NetHelper
from apps.utilities.publiclibrary.SystemInfo import SystemInfo
from apps.utilities.publiclibrary.UserInfo import UserInfo
from apps.hadmin.MvcAppUtilties.CommonUtils import CommonUtils



def index(request):
    return render(request, 'Login/Index.html')

def checklogin(request):
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
                    # request.session['Account'] = Account
                    # request.session['Password'] = Password
                    # OnLineCount = cache.get('OnLineCount', [])
                    # if OnLineCount:
                    #     online_ips = cache.get_many(OnLineCount).keys()
                    # if Account in OnLineCount:
                    #     cache.set("OnLineCount", OnLineCount)
                    # else:
                    #     OnLineCount.append(Account)
                    #     cache.set("OnLineCount", OnLineCount)



                    Msg = '3'
                    response = HttpResponse(Msg)
                    CommonUtils.AddCurrent(imanageuser, response, request)
                    response.set_cookie('UIStyle', CommonUtils.UIStyle(response, request))
                    return response
                else:
                    Msg = '4'
                    return HttpResponse(Msg)
        except Exception as e:
            print(e)