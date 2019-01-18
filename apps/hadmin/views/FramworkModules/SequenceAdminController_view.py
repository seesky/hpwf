# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2019/1/17 8:00'

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
from apps.bizlogic.service.base.ItemsService import ItemsService
from apps.bizlogic.service.base.ItemDetailsService import ItemDetailsService
from django.db.models import Q
from apps.bizlogic.service.base.SequenceService import SequenceService


def BuildToolBarButton(response, request):
    sb = ''
    linkbtnTemplate = "<a id=\"a_{0}\" class=\"easyui-linkbutton\" style=\"float:left\"  plain=\"true\" href=\"javascript:;\" icon=\"{1}\"  {2} title=\"{3}\">{4}</a>"
    sb = sb + "<a id=\"a_refresh\" class=\"easyui-linkbutton\" style=\"float:left\"  plain=\"true\" href=\"javascript:;\" icon=\"icon16_arrow_refresh\"  title=\"重新加载\">刷新</a> "
    sb = sb + "<div class='datagrid-btn-separator'></div> "
    sb = sb + linkbtnTemplate.format("add", "icon16_table_add", "" if PublicController.IsAuthorized(response, request, "SequenceAdmin.Add") else "disabled=\"True\"", "新增序列", "新增")
    sb = sb + linkbtnTemplate.format("edit", "icon16_table_edit", "" if PublicController.IsAuthorized(response, request, "SequenceAdmin.Edit") else "disabled=\"True\"", "修改选中序列", "修改")
    sb = sb + linkbtnTemplate.format("del", "icon16_table_delete", "" if PublicController.IsAuthorized(response, request, "SequenceAdmin.Delete") else "disabled=\"True\"", "删除选中序列", "删除")
    sb = sb + "<div class='datagrid-btn-separator'></div> "
    sb = sb + linkbtnTemplate.format("export", "icon16_table_export", "" if PublicController.IsAuthorized(response, request, "ParameterAdmin.Export") else "disabled=\"True\"", "导出序列数据", "导出")
    return sb


@LoginAuthorize
def Index(request):
    """
    起始页
    Args:
    Returns:
    """
    response = HttpResponse()
    tmp = loader.get_template('SequenceAdmin/Index.html')  # 加载模板
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
        rows = 20

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

    recordCount, dtParameter = SequenceService.GetDTByPage(None, SearchFilter.TransfromFilterToSql(filter, False), rows,  sort + ' ' + order)
    pageValue = dtParameter.page(page)

    sequenceTmp = ''
    for sequence in pageValue:
        sequenceTmp = sequenceTmp + ', ' + json.dumps(sequence, cls=DateEncoder)
    sequenceTmp = sequenceTmp.strip(',')
    returnValue = '{"total": ' + str(recordCount) + ', "rows":[' + sequenceTmp + ']}'

    response.content = returnValue
    return response