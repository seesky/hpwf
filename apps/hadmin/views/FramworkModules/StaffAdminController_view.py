# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2019/1/10 13:38'

from apps.hadmin.MvcAppUtilties.LoginAuthorize import LoginAuthorize
from django.http.response import HttpResponse
from django.template import loader ,Context
from apps.hadmin.MvcAppUtilties.CommonUtils import CommonUtils
from apps.hadmin.MvcAppUtilties.PublicController import PublicController
from apps.hadmin.MvcAppUtilties.AjaxOnly import AjaxOnly
from apps.bizlogic.service.base.StaffService import StaffService


def BuildToolBarButton(response, request):
    sb = ''
    linkbtnTemplate = "<a id=\"a_{0}\" class=\"easyui-linkbutton\" style=\"float:left\"  plain=\"true\" href=\"javascript:;\" icon=\"{1}\"  {2} title=\"{3}\">{4}</a>"
    sb = sb + "<a id=\"a_refresh\" class=\"easyui-linkbutton\" style=\"float:left\"  plain=\"true\" href=\"javascript:;\" icon=\"icon16_arrow_refresh\"  title=\"重新加载\">刷新</a> "
    sb = sb + "<div class='datagrid-btn-separator'></div> "
    sb = sb + linkbtnTemplate.format("AddStaff", "icon16_user_add", "" if PublicController.IsAuthorized(response, request, "StaffAdmin.Add") else "disabled=\"True\"", "添加员工", "添加")
    sb = sb + linkbtnTemplate.format("EditStaff", "icon16_user_edit", "" if PublicController.IsAuthorized(response, request, "StaffAdmin.Edit") else "disabled=\"True\"", "修改员工", "修改")
    sb = sb + linkbtnTemplate.format("DeleteStaff", "icon16_user_delete", "" if PublicController.IsAuthorized(response, request, "StaffAdmin.Delete") else "disabled=\"True\"", "删除员工", "删除")
    sb = sb + "<div class='datagrid-btn-separator'></div> "
    sb = sb + linkbtnTemplate.format("MoveTo", "icon16_arrow_switch", "" if PublicController.IsAuthorized(response, request, "StaffAdmin.Move") else "disabled=\"True\"", "移动选中的员工", "移动")
    sb = sb + "<div class='datagrid-btn-separator'></div> "
    sb = sb + linkbtnTemplate.format("Export", "icon16_user_go", "" if PublicController.IsAuthorized(response, request, "StaffAdmin.Export") else "disabled=\"True\"", "导出员工数据", "导出")
    return sb

@LoginAuthorize
def Index(request):
    """
    起始页
    Args:
    Returns:
    """
    response = HttpResponse()
    tmp = loader.get_template('StaffAdmin/Index.html')  # 加载模板
    render_content = {'Skin': CommonUtils.Theme(response, request),
                      'ToolButton': BuildToolBarButton(response, request)}  # 将要渲染到模板的数据
    new_body = tmp.render(render_content)  # 渲染模板
    response.content = new_body  # 设置返回内容
    return response

@AjaxOnly
@LoginAuthorize
def GetStaffByOrganizeId(request):
    """
    起始页
    Args:
    Returns:
    """
    jsons = "[]"
    organizeId = None
    try:
        organizeId = request.POST['organizeId']
    except:
        organizeId = None

    response = HttpResponse()
    returnValue = '['

    if organizeId:
        recordCount = 0
        dtStaff = StaffService.GetDTByOrganize(None, organizeId, True)
        for staff in dtStaff:
            returnValue = returnValue + staff.toJSON() + ","
        returnValue = returnValue.strip(",")
        returnValue = returnValue + "]"
        response.content = returnValue
    else:
        response.content = jsons

    return response