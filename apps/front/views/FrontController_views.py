# _*_ coding: utf-8 _*_
__author__ = 'baxuelong@163.com'
__date__ = '2019/2/28 8:09'

from apps.hadmin.MvcAppUtilties.LoginAuthorize import LoginAuthorize
from apps.hadmin.MvcAppUtilties.IsAuthorized import IsAuthorized
from django.http.response import HttpResponse
from django.template import loader
from apps.hadmin.MvcAppUtilties.CommonUtils import CommonUtils

@LoginAuthorize
@IsAuthorized("Front.IndexManage")
def IndexManage(request):
    """
    前台管理主页
    """
    response = HttpResponse()
    tmp = loader.get_template('Front/IndexManage.html')  # 加载模板
    render_content = {}  # 将要渲染到模板的数据
    new_body = tmp.render(render_content)  # 渲染模板
    response.content = new_body  # 设置返回内容
    return response

def Index(request):
    """
    前台主页
    """
    response = HttpResponse()
    tmp = loader.get_template('Front/Index.html')  # 加载模板
    render_content = {}  # 将要渲染到模板的数据
    new_body = tmp.render(render_content)  # 渲染模板
    response.content = new_body  # 设置返回内容
    return response