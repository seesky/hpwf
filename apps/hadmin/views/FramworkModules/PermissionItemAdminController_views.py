# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2019/1/14 7:56'

from apps.hadmin.MvcAppUtilties.CommonUtils import CommonUtils
from apps.hadmin.MvcAppUtilties.PublicController import PublicController
from apps.hadmin.MvcAppUtilties.LoginAuthorize import LoginAuthorize
from django.http.response import HttpResponse
from django.template import loader ,Context

def BuildToolBarButton(response, request):
    sb = ''
    linkbtnTemplate = "<a id=\"a_{0}\" class=\"easyui-linkbutton\" style=\"float:left\"  plain=\"true\" href=\"javascript:;\" icon=\"{1}\"  {2} title=\"{3}\">{4}</a>"
    sb = sb + "<a id=\"a_refresh\" class=\"easyui-linkbutton\" style=\"float:left\"  plain=\"true\" href=\"javascript:;\" icon=\"icon16_arrow_refresh\"  title=\"重新加载\">刷新</a> "
    sb = sb + "<div class='datagrid-btn-separator'></div> "
    sb = sb + linkbtnTemplate.format("add", "icon16_layout_add", "" if PublicController.IsAuthorized(response, request, "PermissionItemManagement.Add") else "disabled=\"True\"", "新增操作权限", "新增")
    sb = sb + linkbtnTemplate.format("edit", "icon16_layout_edit", "" if PublicController.IsAuthorized(response, request, "PermissionItemManagement.Edit") else "disabled=\"True\"", "修改操作权限", "修改")
    sb = sb + linkbtnTemplate.format("del", "icon16_layout_delete", "" if PublicController.IsAuthorized(response, request, "PermissionItemManagement.Delete") else "disabled=\"True\"", "删除操作权限", "删除")
    sb = sb + "<div class='datagrid-btn-separator'></div> "
    sb = sb + linkbtnTemplate.format("move", "icon16_arrow_switch", "" if PublicController.IsAuthorized(response, request, "PermissionItemManagement.Move") else "disabled=\"True\"", "移动选中的操作权限", "移动")
    sb = sb + linkbtnTemplate.format("export", "icon16_export_excel", "" if PublicController.IsAuthorized(response, request,  "PermissionItemManagement.Export") else "disabled=\"True\"", "导出操作权限列表", "导出")
    sb = sb + "<div class='datagrid-btn-separator'></div> "
    sb = sb + linkbtnTemplate.format("setuserpermissionitemepermission", "icon16_view_bandwidth_usage", "" if PublicController.IsAuthorized(response, request, "PermissionItemManagement.UserPermissionItem") else "disabled=\"True\"", "设置用户的操作权限项访问权限", "用户操作权限")
    sb = sb + linkbtnTemplate.format("setrolepermissionitemepermission", "icon16_key", "" if PublicController.IsAuthorized(response, request, "PermissionItemManagement.RolePermissionItem") else "disabled=\"True\"", "设置角色的操作权限项访问权限", "角色操作权限")
    return sb


@LoginAuthorize
def Index(request):
    """
    起始页
    Args:
    Returns:
    """
    response = HttpResponse()
    tmp = loader.get_template('PermissionItemAdmin/Index.html')  # 加载模板
    render_content = {'Skin': CommonUtils.Theme(response, request),
                      'ToolButton': BuildToolBarButton(response, request)}  # 将要渲染到模板的数据
    new_body = tmp.render(render_content)  # 渲染模板
    response.content = new_body  # 设置返回内容
    return response