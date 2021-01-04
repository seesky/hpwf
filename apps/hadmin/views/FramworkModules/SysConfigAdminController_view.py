# _*_ coding: utf-8 _*_
__author__ = 'baxuelong@163.com'
__date__ = '2019/2/14 8:44'

from apps.hadmin.MvcAppUtilties.CommonUtils import CommonUtils
from apps.hadmin.MvcAppUtilties.PublicController import PublicController
from apps.hadmin.MvcAppUtilties.LoginAuthorize import LoginAuthorize
from django.http.response import HttpResponse
from django.template import loader ,Context
from apps.bizlogic.service.base.ParameterService import ParameterService
import json

@LoginAuthorize
def Index(request):
    """
    起始页
    Args:
    Returns:
    """
    response = HttpResponse()
    tmp = loader.get_template('SysConfig/Index.html')  # 加载模板
    render_content = {'Skin': CommonUtils.Theme(response, request)}  # 将要渲染到模板的数据
    new_body = tmp.render(render_content)  # 渲染模板
    response.content = new_body  # 设置返回内容
    return response

@LoginAuthorize
def GetDefaultConfig(request):
    response = HttpResponse()
    vUser = CommonUtils.Current(response, request)
    curTheme = ParameterService.GetParameter(vUser, "User", vUser.Id, "WebTheme")
    curPageSize = ParameterService.GetParameter(vUser, "User", vUser.Id, "WebPageSize")
    curNavType = ParameterService.GetParameter(vUser, "User", vUser.Id, "NavType")

    if curTheme:
        if ParameterService.GetServiceConfig(CommonUtils.Current(response, request), 'LoginProvider') == 'Cookie':
            response.set_signed_cookie('theme', curTheme,
                                       max_age=int(
                                           ParameterService.GetServiceConfig(CommonUtils.Current(response, request),
                                                                             'CookieMaxAge')),
                                       salt=ParameterService.GetServiceConfig(CommonUtils.Current(response, request),
                                                                              'LoginUserKey'))

    outJson = "{"
    if curTheme:
        outJson = outJson + "\"theme\":{\"title\":\"默认皮肤\",\"name\":\"" + curTheme + "\",\"selected\":true}"
    else:
        outJson = outJson + "\"theme\":{\"title\":\"默认皮肤\",\"name\":\"default\",\"selected\":true}"

    if curPageSize:
        outJson = outJson + ",\"gridRows\":" + curPageSize
    else:
        outJson = outJson + ",\"gridRows\":20"

    if curNavType:
        outJson = outJson + ",\"navType\":\"" + curNavType + "\"}"
    else:
        outJson = outJson + ",\"navType\":\"AccordionTree\"}"

    response.content = outJson
    return response

@LoginAuthorize
def UpdateUserConfig(request):

    if request.POST['themeJson']:

        response = HttpResponse()
        vUser = CommonUtils.Current(response, request)

        jobj = json.loads(request.POST['themeJson'])
        pageSize = str(jobj['gridRows'])
        themeName = str(jobj['theme']['name'])
        navType = str(jobj['navType'])
        returnValue = 0

        if pageSize:
            returnValue = returnValue + ParameterService.SetParameter(vUser, "User", vUser.Id, "WebPageSize", pageSize)
        if themeName:
            returnValue = returnValue + ParameterService.SetParameter(vUser, "User", vUser.Id, "WebTheme", themeName)
            response.set_signed_cookie('theme', themeName,
                                       max_age=int(
                                           ParameterService.GetServiceConfig(CommonUtils.Current(response, request),
                                                                             'CookieMaxAge')),
                                       salt=ParameterService.GetServiceConfig(CommonUtils.Current(response, request),
                                                                              'LoginUserKey'))
        if navType:
            returnValue = returnValue + ParameterService.SetParameter(vUser, "User", vUser.Id, "NavType", navType)
            response.set_signed_cookie('UIStyle', navType,
                                       max_age=int(
                                           ParameterService.GetServiceConfig(CommonUtils.Current(response, request),
                                                                             'CookieMaxAge')),
                                       salt=ParameterService.GetServiceConfig(CommonUtils.Current(response, request),
                                                                              'LoginUserKey'))
        if returnValue > 0:
            response.content = '1'
        else:
            response.content = '保存失败！'
        return response
    else:
        response = HttpResponse()
        response.content = "无保存数据！"
        return response



