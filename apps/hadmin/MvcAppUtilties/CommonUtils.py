# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2019/1/4 17:02'

from apps.bizlogic.service.base.ParameterService import ParameterService
import pickle
import json


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
                user = pickle.dumps(user)
                response.set_signed_cookie(ParameterService.GetServiceConfig('LoginProvider'), str(user), max_age=int(ParameterService.GetServiceConfig('CookieMaxAge')), salt=ParameterService.GetServiceConfig('LoginUserKey'))
            else:
                user = pickle.dumps(user)
                request.session[ParameterService.GetServiceConfig('LoginProvider')] = str(user)
        except Exception as e:
            print(e)


    def Current(response, request):
        if ParameterService.GetServiceConfig('LoginProvider') == 'Cookie':
            try:
                user = request.get_signed_cookie(ParameterService.GetServiceConfig('LoginProvider'), salt=ParameterService.GetServiceConfig('LoginUserKey'))
                user =  pickle.loads(user)
                return user
            except Exception as e:
                return None
        else:
            pass

    def UIStyle(response, request):
        tmpUIStyle = "AccordionTree"
        vUser = CommonUtils.Current(response, request)
        if vUser:
            tmpUIStyle = ParameterService.GetParameter('User', vUser.Id, 'NavType')
        else:
            tmpUIStyle = 'AccordionTree'

        request.session['UIStyle'] = tmpUIStyle
        response.set_signed_cookie('UIStyle', tmpUIStyle,
                                   max_age=int(ParameterService.GetServiceConfig('CookieMaxAge')),
                                   salt=ParameterService.GetServiceConfig('LoginUserKey'))
        return tmpUIStyle