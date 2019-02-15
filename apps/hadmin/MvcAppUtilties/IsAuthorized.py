# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2019/2/15 9:33'

from apps.bizlogic.service.base.ParameterService import ParameterService
from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from apps.utilities.publiclibrary.SecretHelper import SecretHelper
import json
from apps.utilities.publiclibrary.UserInfo import UserInfo
from apps.hadmin.MvcAppUtilties.PublicController import PublicController
from django.http.response import HttpResponse
from functools import wraps



def IsAuthorized(code):
    def authorized(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            if ParameterService.GetServiceConfig(None, 'LoginProvider') == 'Cookie':
                try:
                    user = args[0].get_signed_cookie(ParameterService.GetServiceConfig(None, 'LoginProvider'),
                                                     salt=ParameterService.GetServiceConfig(None, 'LoginUserKey'))
                    if user:
                        user = SecretHelper.AESDecrypt(user)
                        try:
                            user = json.loads(user, object_hook=UserInfo.json_2_obj)
                            if PublicController.IsAuthorized(HttpResponse(), args[0], code):
                                return func(*args, **kwargs)
                            else:
                                return HttpResponseRedirect('/Admin/Index/')
                        except:
                            return HttpResponseRedirect('/Admin/Index/')
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
                            if PublicController.IsAuthorized(HttpResponse(), args[0], code):
                                return func(*args, **kwargs)
                            else:
                                return HttpResponseRedirect('/Admin/Index/')
                        except:
                            return HttpResponseRedirect('/Admin/Index/')
                    else:
                        return HttpResponseRedirect('/Admin/Index/')
                except Exception as e:
                    print(e)
                    return HttpResponseRedirect('/Admin/Index/')

        return wrapped_function
    return authorized