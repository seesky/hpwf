# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2019/1/7 11:19'

from apps.bizlogic.service.base.ParameterService import ParameterService
from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from apps.utilities.publiclibrary.SecretHelper import SecretHelper
import json
from apps.utilities.publiclibrary.UserInfo import UserInfo
from apps.bizlogic.service.base.ExceptionService import ExceptionService
from apps.bizlogic.models import Ciexception
import uuid,datetime

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

        if ParameterService.GetServiceConfig(None, 'LoginProvider') == 'Cookie':
            try:
                user = args[0].get_signed_cookie(ParameterService.GetServiceConfig(None, 'LoginProvider'),
                                                 salt=ParameterService.GetServiceConfig(None, 'LoginUserKey'))
                if user:
                    user = SecretHelper.AESDecrypt(user)

                    try:
                        user = json.loads(user, object_hook=UserInfo.json_2_obj)
                    except:
                        return HttpResponseRedirect('/Admin/Index/')
                    return self.f(*args, **kw)
                else:
                    return HttpResponseRedirect('/Admin/Index/')
            except Exception as e:
                print(e)
                return HttpResponseRedirect('/Admin/Index/')
        else:
            try:
                user = args[0].session.get(ParameterService.GetServiceConfig(None, 'LoginProvider'))
                if user:
                    user = SecretHelper.AESDecrypt(user)
                    try:
                        user = json.loads(user, object_hook=UserInfo.json_2_obj)
                    except:
                        return HttpResponseRedirect('/Admin/Index/')
                    return self.f(*args, **kw)
                else:
                    return HttpResponseRedirect('/Admin/Index/')
            except Exception as e:
                print(e)
                #TODO:这个地方只是暂时用来记录异常信息的代码，应当将不同模块不同方法的异常记录写到各自的代码中，后期此代码要删除
                e_out = Ciexception()
                e_out.id = uuid.uuid4()
                e_out.createon = datetime.datetime.now()
                e_out.message = e
                ExceptionService.Add(None, e_out)

                return HttpResponseRedirect('/Admin/Index/')