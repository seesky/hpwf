# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2019/1/16 9:00'

from apps.bizlogic.service.base.ExceptionService import ExceptionService
from apps.hadmin.MvcAppUtilties.CommonUtils import CommonUtils
from apps.hadmin.MvcAppUtilties.PublicController import PublicController
from apps.hadmin.MvcAppUtilties.LoginAuthorize import LoginAuthorize
from apps.hadmin.MvcAppUtilties.AjaxOnly import AjaxOnly
from apps.utilities.publiclibrary.SearchFilter import SearchFilter
from django.http.response import HttpResponse
from django.template import loader ,Context
import json
from apps.hadmin.MvcAppUtilties.JsonHelper import DateEncoder


def BuildToolBarButton(response, request):
    sb = ''
    linkbtnTemplate = "<a id=\"a_{0}\" class=\"easyui-linkbutton\" style=\"float:left\"  plain=\"true\" href=\"javascript:;\" icon=\"{1}\"  {2} title=\"{3}\">{4}</a>"
    sb = sb + "<a id=\"a_refresh\" class=\"easyui-linkbutton\" style=\"float:left\"  plain=\"true\" href=\"javascript:;\" icon=\"icon16_arrow_refresh\"  title=\"重新加载\">刷新</a> "
    sb = sb + "<div class='datagrid-btn-separator'></div> "
    sb = sb + linkbtnTemplate.format("ViewDetail", "icon16_table_export", "" if PublicController.IsAuthorized(response, request, "ExceptionAdmin.Query") else "disabled=\"True\"", "查看异常详情", "查看异常详情")
    sb = sb + "<div class='datagrid-btn-separator'></div> "
    sb = sb + linkbtnTemplate.format("Export", "icon16_table_export", "" if PublicController.IsAuthorized(response, request, "ExceptionAdmin.Export") else "disabled=\"True\"", "导出系统异常数据", "导出")
    sb = sb + linkbtnTemplate.format("Delete", "icon16_table_delete", "" if PublicController.IsAuthorized(response, request, "ExceptionAdmin.Delete") else "disabled=\"True\"", "删除系统异常", "删除")
    return sb


@LoginAuthorize
def Index(request):
    """
    起始页
    Args:
    Returns:
    """
    response = HttpResponse()
    tmp = loader.get_template('ExceptionAdmin/Index.html')  # 加载模板
    render_content = {'Skin': CommonUtils.Theme(response, request),
                      'ToolButton': BuildToolBarButton(response, request)}  # 将要渲染到模板的数据
    new_body = tmp.render(render_content)  # 渲染模板
    response.content = new_body  # 设置返回内容
    return response

@LoginAuthorize
def GridPageListJson(request):
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
        sort = 'createon'

    try:
        order = request.POST['order']
    except:
        order = 'desc'

    try:
        filter = request.POST['filter']
    except:
        filter = ''

    response = HttpResponse()

    recordCount = 0
    recordCount, dtLog = ExceptionService.GetDTByPage(page, rows, SearchFilter.TransfromFilterToSql(filter, False),
                                                sort + " " + order)

    excTmp = ''
    for log in dtLog:
        excTmp = excTmp + ', ' + json.dumps(log, cls=DateEncoder)
        excTmp = excTmp.strip(',')
    returnValue = '{"total": ' + str(recordCount) + ', "rows":[' + excTmp + ']}'

    response.content = returnValue
    return response