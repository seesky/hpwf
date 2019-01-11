# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2019/1/7 11:19'

from apps.bizlogic.service.base.ParameterService import ParameterService
from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from apps.utilities.publiclibrary.SecretHelper import SecretHelper
import json
from apps.utilities.publiclibrary.UserInfo import UserInfo

class LoginAuthorize(object):

    def __init__(self, func):
        self.f = func

    # def __call__(self, request):
    #
    #     if ParameterService.GetServiceConfig('LoginProvider') == 'Cookie':
    #         try:
    #             user = request.get_signed_cookie(ParameterService.GetServiceConfig('LoginProvider'),
    #                                              salt=ParameterService.GetServiceConfig('LoginUserKey'))
    #             if user:
    #                 user = SecretHelper.AESDecrypt(user)
    #
    #                 try:
    #                     user = json.loads(user, object_hook=UserInfo.json_2_obj)
    #                 except:
    #                     return HttpResponseRedirect('/admin/index/')
    #                 return self.f(request)
    #             else:
    #                 return HttpResponseRedirect('/admin/index/')
    #         except Exception as e:
    #             print(e)
    #             return HttpResponseRedirect('/admin/index/')

    def __call__(self, *args, **kw):

        if ParameterService.GetServiceConfig('LoginProvider') == 'Cookie':
            try:
                user = args[0].get_signed_cookie(ParameterService.GetServiceConfig('LoginProvider'),
                                                 salt=ParameterService.GetServiceConfig('LoginUserKey'))
                if user:
                    user = SecretHelper.AESDecrypt(user)

                    try:
                        user = json.loads(user, object_hook=UserInfo.json_2_obj)
                    except:
                        return HttpResponseRedirect('/admin/index/')
                    return self.f(*args, **kw)
                else:
                    return HttpResponseRedirect('/admin/index/')
            except Exception as e:
                print(e)
                return HttpResponseRedirect('/admin/index/')
