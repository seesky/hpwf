# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2019/1/10 14:33'

from apps.hadmin.MvcAppUtilties.LoginAuthorize import LoginAuthorize
from django.http.response import HttpResponse
from django.template import loader ,Context
from apps.hadmin.MvcAppUtilties.CommonUtils import CommonUtils
from apps.hadmin.MvcAppUtilties.PublicController import PublicController
from apps.hadmin.MvcAppUtilties.AjaxOnly import AjaxOnly
from apps.bizlogic.service.base.RoleService import RoleService
from apps.utilities.publiclibrary.SearchFilter import SearchFilter
import json
from apps.hadmin.MvcAppUtilties.JsonHelper import DateEncoder
from apps.bizlogic.service.base.ItemDetailsService import ItemDetailsService
from apps.bizlogic.service.base.RoleService import RoleService

def BuildToolBarButton(response, request):
    sb = ''
    linkbtnTemplate = "<a id=\"a_{0}\" class=\"easyui-linkbutton\" style=\"float:left\"  plain=\"true\" href=\"javascript:;\" icon=\"{1}\"  {2} title=\"{3}\">{4}</a>"
    sb = sb + "<a id=\"a_refresh\" class=\"easyui-linkbutton\" style=\"float:left\"  plain=\"true\" href=\"javascript:;\" icon=\"icon16_arrow_refresh\"  title=\"重新加载\">刷新</a> "
    sb = sb + "<div class='datagrid-btn-separator'></div> "
    sb = sb + linkbtnTemplate.format("add", "icon16_group_add", "" if PublicController.IsAuthorized(response, request, "RoleManagement.Add") else "disabled=\"True\"", "新增角色", "新增")
    sb = sb + linkbtnTemplate.format("edit", "icon16_group_edit", "" if PublicController.IsAuthorized(response, request, "RoleManagement.Edit") else "disabled=\"True\"", "修改选中角色", "修改")
    sb = sb + linkbtnTemplate.format("del", "icon16_group_delete", "" if PublicController.IsAuthorized(response, request, "RoleManagement.Delete") else "disabled=\"True\"", "删除选中角色", "删除")
    sb = sb + "<div class='datagrid-btn-separator'></div> "
    sb = sb + linkbtnTemplate.format("roleuser", "icon16_group_link", "" if PublicController.IsAuthorized(response, request, "RoleManagement.RoleUser") else "disabled=\"True\"", "设置当前角色拥有的用户", "角色用户设置")
    sb = sb + "<div class='datagrid-btn-separator'></div> "
    sb = sb + linkbtnTemplate.format("export", "icon16_group_go", "" if PublicController.IsAuthorized(response, request, "RoleManagement.Export") else "disabled=\"True\"", "导出角色数据", "导出")
    sb = sb + linkbtnTemplate.format("print", "icon16_printer", "" if PublicController.IsAuthorized(response, request, "RoleManagement.Export") else "disabled=\"True\"", "打印", "打印")
    return sb


@LoginAuthorize
def Index(request):
    """
    起始页
    Args:
    Returns:
    """
    response = HttpResponse()
    tmp = loader.get_template('RoleAdmin/Index.html')  # 加载模板
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

    recordCount = 0
    dtRole = RoleService.GetDtByPage(None, rows, SearchFilter.TransfromFilterToSql(filter, False), sort + ' ' + order)
    recordCount = dtRole.count
    pageValue = dtRole.page(page)

    roleTmp = ''
    for role in pageValue:
        roleTmp = roleTmp + ', ' + json.dumps(role, cls=DateEncoder)
    roleTmp = roleTmp.strip(',')
    returnValue = '{"total": ' + str(recordCount) + ', "rows":[' + roleTmp + ']}'

    response.content = returnValue
    return response

@LoginAuthorize
def GetRoleCategory(request):
    categoryCode = None
    try:
        categoryCode = request.GET['categoryCode']
    except:
        categoryCode = None

    response = HttpResponse()
    dtItemDetail = ItemDetailsService.GetDTByCode(None, categoryCode)

    jsons = ''
    jsons = jsons + '['
    jsons = jsons + '{"ITEMCODE": null,"ITEMNAME": "==选择所有分类==","ITEMVALUE": "0"},'
    for item in dtItemDetail:
        jsons = jsons + '{"ITEMCODE": "' + item.itemcode + '","ITEMNAME": "' + item.itemname + '","ITEMVALUE": "' + item.itemvalue + '"},'
    jsons = jsons.strip(',')
    jsons = jsons + ']'
    response.content = jsons
    return response

@LoginAuthorize
def GetRoleListByOrganize(request):
    organizeId = None
    try:
        organizeId = request.POST['organizeId']
    except:
        organizeId = None

    response = HttpResponse()
    writeJson = "[]"
    tempJson = "["
    if organizeId:
        roles = RoleService.GetDTByOrganize(None, organizeId, True)
        for role in roles:
            tempJson = tempJson + str(role.toJSON()) + ","
        tempJson = tempJson.strip(",")
        tempJson = tempJson + "]"
        response.content = tempJson
        return response
    else:
        response.content = writeJson
        return response

@LoginAuthorize
def GetEnabledRoleList(request):
    returnValue = "[]"
    dtRole = RoleService.GetDTByValues(None, {'deletemark':0, 'enabled':1})
    if dtRole and len(dtRole) > 0:
        returnValue = '['
        for role in dtRole:
            returnValue = returnValue + role.toJSON() + ","
        returnValue = returnValue.strip(",")
        returnValue = returnValue + "]"

        response = HttpResponse()
        response.content = returnValue
        return response

    return returnValue