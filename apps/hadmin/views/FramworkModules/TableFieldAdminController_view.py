# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2019/1/18 9:55'

from apps.bizlogic.service.base.TableColumnsService import TableColumnsService
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
    sb = sb + linkbtnTemplate.format("BatchSave", "icon16_save_data", "" if PublicController.IsAuthorized(response, request, "TableFieldAdmin.BatchSave") else "disabled=\"True\"", "批量保存", "批量保存")
    sb = sb + linkbtnTemplate.format("BatchSet", "icon16_table_format", "" if PublicController.IsAuthorized(response, request, "TableFieldAdmin.BatchSave") else "disabled=\"True\"", "批量设置", "批量设置")
    sb = sb + linkbtnTemplate.format("Export", "icon16_table_export", "" if PublicController.IsAuthorized(response, request, "TableFieldAdmin.Export") else "disabled=\"True\"", "导出", "导出")
    sb = sb + "<div class='datagrid-btn-separator'></div> "
    sb = sb + linkbtnTemplate.format("SetTablePermission", "icon16_table_lightning", "" if PublicController.IsAuthorized(response, request, "TableFieldAdmin.SetTablePermission") else "disabled=\"True\"", "设置权限控制表", "设置权限控制表")
    return sb


@LoginAuthorize
def Index(request):
    """
    起始页
    Args:
    Returns:
    """
    response = HttpResponse()
    tmp = loader.get_template('TableFieldAdmin/Index.html')  # 加载模板
    render_content = {'Skin': CommonUtils.Theme(response, request),
                      'ToolButton': BuildToolBarButton(response, request)}  # 将要渲染到模板的数据
    new_body = tmp.render(render_content)  # 渲染模板
    response.content = new_body  # 设置返回内容
    return response

@AjaxOnly
@LoginAuthorize
def GetTableNameAndCode(request):
    dtTableList = TableColumnsService.GetTableNameAndCode(None)
    returnValue = '['
    for table in dtTableList:
        returnValue = returnValue + json.dumps(table) + ","
    returnValue = returnValue.strip(",")
    returnValue = returnValue + "]"

    response = HttpResponse()
    response.content = returnValue
    return response

@AjaxOnly
@LoginAuthorize
def GetDTByTable(request):

    try:
        tableCode = request.POST['tableCode']
    except:
        tableCode = ''

    dtTableColumns = TableColumnsService.GetDTByTable(tableCode)

    returnValue = '['
    for columns in dtTableColumns:
        returnValue = returnValue + columns.toJSON() + ","
    returnValue = returnValue.strip(",")
    returnValue = returnValue + "]"

    response = HttpResponse()
    response.content = returnValue
    return response