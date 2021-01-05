#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'baxuelong@163.com'
__date__ = '2021/1/5 16:22'

from django.http.response import HttpResponse
from apps.hadmin.MvcAppUtilties.LoginAuthorize import LoginAuthorize
from django.template import loader ,Context
from apps.hadmin.MvcAppUtilties.CommonUtils import CommonUtils
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@LoginAuthorize
def Index(request):
    """
    起始页
    Args:
    Returns:
    """
    response = HttpResponse()
    tmp = loader.get_template('MyParticipantTask/Index.html')  # 加载模板
    render_content = {'Skin': CommonUtils.Theme(response, request)}  # 将要渲染到模板的数据
    new_body = tmp.render(render_content)  # 渲染模板
    response.content = new_body  # 设置返回内容
    return response