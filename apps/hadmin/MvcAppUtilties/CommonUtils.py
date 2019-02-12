# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2019/1/4 17:02'

from apps.bizlogic.service.base.ParameterService import ParameterService
import pickle
import json
from apps.utilities.publiclibrary.SecretHelper import SecretHelper
import zlib
from apps.utilities.publiclibrary.UserInfo import UserInfo
from django.db.models import Q

class CommonUtils(object):

    def AddCurrent(user, response, request):
        """
        写入登录信息
        Args:
            user (UserInfo): user
        Returns:
        """
        try:
            if ParameterService.GetServiceConfig('LoginProvider') == 'Cookie':
                #user = pickle.dumps(user)
                user = json.dumps(user, default=UserInfo.obj_2_json)
                #response.set_signed_cookie(ParameterService.GetServiceConfig('LoginProvider'), str(user), max_age=int(ParameterService.GetServiceConfig('CookieMaxAge')), salt=ParameterService.GetServiceConfig('LoginUserKey'))
                user = SecretHelper.AESEncrypt(user)
                user = str(user, encoding = "utf8")
                response.set_signed_cookie(ParameterService.GetServiceConfig('LoginProvider'), user,
                                           max_age=int(ParameterService.GetServiceConfig('CookieMaxAge')),
                                           salt=ParameterService.GetServiceConfig('LoginUserKey'))
            else:
                #user = pickle.dumps(user)
                user = json.dumps(user, default=UserInfo.obj_2_json)
                request.session[ParameterService.GetServiceConfig('LoginProvider')] = user
        except Exception as e:
            print(e)

    def EmptyCurrent(response):
        try:
            if ParameterService.GetServiceConfig('LoginProvider') == 'Cookie':
                response.delete_cookie(ParameterService.GetServiceConfig('LoginProvider'))
            else:
                pass
        except Exception as e:
            print(e)

    def Current(response, request):
        if ParameterService.GetServiceConfig('LoginProvider') == 'Cookie':
            try:
                user = request.get_signed_cookie(ParameterService.GetServiceConfig('LoginProvider'), salt=ParameterService.GetServiceConfig('LoginUserKey'))
                #user =  pickle.loads(user)
                user = SecretHelper.AESDecrypt(user)
                user = json.loads(user, object_hook=UserInfo.json_2_obj)
                return user
            except Exception as e:
                return None
        else:
            pass

    def UIStyle(response, request):
        tmpUIStyle = "AccordionTree"
        vUser = CommonUtils.Current(response, request)
        if vUser:
            try:
                tmpUIStyle = ParameterService.GetParameter('User', vUser.Id, 'NavType')
            except:
                tmpUIStyle = 'AccordionTree'
        else:
            tmpUIStyle = 'AccordionTree'

        request.session['UIStyle'] = tmpUIStyle
        response.set_signed_cookie('UIStyle', tmpUIStyle,
                                   max_age=int(ParameterService.GetServiceConfig('CookieMaxAge')),
                                   salt=ParameterService.GetServiceConfig('LoginUserKey'))
        return tmpUIStyle

    def Theme(response, request):
        tmpTheme = "default"
        vUser = CommonUtils.Current(response, request)
        if vUser:
                tmpTheme = ParameterService.GetParameter('User', vUser.Id, 'WebTheme')
        if not tmpTheme:
            tmpTheme = 'default'

        request.session['theme'] = tmpTheme
        response.set_signed_cookie('theme', tmpTheme,
                                   max_age=int(ParameterService.GetServiceConfig('CookieMaxAge')),
                                   salt=ParameterService.GetServiceConfig('LoginUserKey'))
        return tmpTheme

    def CheckTreeParentId(dataTable, fieldId, fieldParentId):
        """
        查找 ParentId 字段的值是否在 Id字段 里
        Args:
            dataTable (): 数据表
            fieldId (string): 主键字段
            fieldParentId (string): 父节点字段
        Returns:
        """
        if not dataTable:
            return;

        for row in dataTable:
            value = row.parentid
            if value:
                if len(dataTable.filter(Q(id=row.parentid))) == 0:
                    row.parentid = '#'
            else:
                row.parentid = "#"
        return dataTable
