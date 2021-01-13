#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'baxuelong@163.com'
__date__ = '2021/1/13 16:08'

from django.http.response import HttpResponse
from apps.hadmin.MvcAppUtilties.LoginAuthorize import LoginAuthorize
from django.template import loader ,Context
from apps.hadmin.MvcAppUtilties.CommonUtils import CommonUtils
from django.views.decorators.csrf import csrf_exempt
from apps.hadmin.MvcAppUtilties.AjaxOnly import AjaxOnly
from apps.bizlogic.service.workflow.WorkFlowUserControl import WorkFlowUserControl
from apps.utilities.publiclibrary.SearchFilter import SearchFilter
import json
from apps.hadmin.MvcAppUtilties.JsonHelper import DateEncoder

@csrf_exempt
@LoginAuthorize
def Index(request):
    """
    起始页
    Args:
    Returns:
    """
    response = HttpResponse()
    tmp = loader.get_template('UserFormAdmin/Index.html')  # 加载模板
    render_content = {'Skin': CommonUtils.Theme(response, request)}  # 将要渲染到模板的数据
    new_body = tmp.render(render_content)  # 渲染模板
    response.content = new_body  # 设置返回内容
    return response


@csrf_exempt
@LoginAuthorize
def MainUserControl(request):
    """
    起始页
    Args:
    Returns:
    """
    response = HttpResponse()
    tmp = loader.get_template('UserFormAdmin/MainUserControl.html')  # 加载模板
    render_content = {'Skin': CommonUtils.Theme(response, request)}  # 将要渲染到模板的数据
    new_body = tmp.render(render_content)  # 渲染模板
    response.content = new_body  # 设置返回内容
    return response

@csrf_exempt
@LoginAuthorize
def UserControlForm(request):
    """
    起始页
    Args:
    Returns:
    """
    response = HttpResponse()
    tmp = loader.get_template('UserFormAdmin/UserControlForm.html')  # 加载模板
    render_content = {'Skin': CommonUtils.Theme(response, request)}  # 将要渲染到模板的数据
    new_body = tmp.render(render_content)  # 渲染模板
    response.content = new_body  # 设置返回内容
    return response

@csrf_exempt
@LoginAuthorize
def MainUserControlLink(request):
    """
    起始页
    Args:
    Returns:
    """
    response = HttpResponse()
    tmp = loader.get_template('UserFormAdmin/MainUserControlLink.html.html')  # 加载模板
    render_content = {'Skin': CommonUtils.Theme(response, request)}  # 将要渲染到模板的数据
    new_body = tmp.render(render_content)  # 渲染模板
    response.content = new_body  # 设置返回内容
    return response


@csrf_exempt
@LoginAuthorize
def GetUserControlClass(request):
    response = HttpResponse()
    returnValue = '[{"id":"0","text":"表单管理","iconCls":"icon16_table_multiple","state":"open","children":[{"id":"1","text":"主表单管理","iconCls":"icon16_page_white_text","state":"open"},{"id":"2","text":"子表单管理","iconCls":"icon16_page_white_text","state":"open"}]}]'
    response.content = returnValue
    return response

@AjaxOnly
@LoginAuthorize
def GetMainUserControlByPage(request):
    page = None
    rows = None
    sort = None
    order = None
    filter = None
    try:
        page = request.POST['page']
    except:
        page = 1

    try:
        rows = request.POST['rows']
    except:
        rows = 50

    try:
        sort = request.POST['sort']
    except:
        sort = 'sortcode'

    try:
        order = request.POST['order']
    except:
        order = 'asc'

    try:
        filter = request.POST['filter']
    except:
        filter = ''

    response = HttpResponse()

    recordCount = 0



    dt = WorkFlowUserControl.GetMainUserControlByPage(CommonUtils.Current(response, request), SearchFilter.TransfromFilterToSql(filter, False), rows, sort + ' ' + order)

    recordCount = dt.count
    pageValue = dt.page(page)

    controlTmp = ''
    for control in pageValue:
        controlTmp = controlTmp + ', ' + json.dumps(control, cls=DateEncoder)
        controlTmp = controlTmp.strip(',')
    returnValue = '{"total": ' + str(recordCount) + ', "rows":[' + controlTmp + ']}'

    response.content = returnValue
    return response


@AjaxOnly
@LoginAuthorize
def GetUserControlByPage(request):
    page = None
    rows = None
    sort = None
    order = None
    filter = None
    try:
        page = request.POST['page']
    except:
        page = 1

    try:
        rows = request.POST['rows']
    except:
        rows = 50

    try:
        sort = request.POST['sort']
    except:
        sort = 'sortcode'

    try:
        order = request.POST['order']
    except:
        order = 'asc'

    try:
        filter = request.POST['filter']
    except:
        filter = ''

    response = HttpResponse()

    recordCount = 0

    dt = WorkFlowUserControl.GetUserInfoByPage(CommonUtils.Current(response, request),
                                                      SearchFilter.TransfromFilterToSql(filter, False), rows,
                                                      sort + ' ' + order)

    recordCount = dt.count
    pageValue = dt.page(page)

    controlTmp = ''
    for control in pageValue:
        controlTmp = controlTmp + ', ' + json.dumps(control, cls=DateEncoder)
        controlTmp = controlTmp.strip(',')
    returnValue = '{"total": ' + str(recordCount) + ', "rows":[' + controlTmp + ']}'

    response.content = returnValue
    return response