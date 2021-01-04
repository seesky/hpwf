# _*_ coding: utf-8 _*_
__author__ = 'baxuelong@163.com'
__date__ = '2019/1/14 10:39'

from apps.hadmin.MvcAppUtilties.CommonUtils import CommonUtils
from apps.hadmin.MvcAppUtilties.PublicController import PublicController
from apps.hadmin.MvcAppUtilties.LoginAuthorize import LoginAuthorize
from apps.hadmin.MvcAppUtilties.AjaxOnly import AjaxOnly
from apps.utilities.publiclibrary.SystemInfo import SystemInfo
from apps.bizlogic.service.base.PermissionItemService import PermissionItemService
from apps.bizlogic.service.permission.ScopPermission import ScopPermission
from django.http.response import HttpResponse
from django.template import loader ,Context
from django.db.models import Q

def GenerateSplitTool():
    sbTool = ''
    sbTool = sbTool + "<div id=\"mm\" style=\"width:100px;\">"
    sbTool = sbTool + "<div id=\"btnRolePermissionScope\" data-options=\"iconCls:'icon16_report_user'\">角色授权范围</div>"
    sbTool = sbTool + "<div id=\"btnRoleTableFieldPermission\" data-options=\"iconCls:'icon16_timeline_marker'\">表字段权限设置</div>"
    sbTool = sbTool + "<div id=\"btnRoleTableConstraintSet\" data-options=\"iconCls:'icon16_script_key'\">约束条件权限设置</div>"
    sbTool = sbTool + "</div>"
    return sbTool

def BuildToolBarButton(response, request):
    sb = ''
    linkbtnTemplate = "<a id=\"btn{0}\" class=\"easyui-linkbutton\" style=\"float:left\"  plain=\"true\" href=\"javascript:;\" icon=\"{1}\"  {2} title=\"{3}\">{4}</a>"
    sb = sb + "<a id=\"a_refresh\" class=\"easyui-linkbutton\" style=\"float:left\"  plain=\"true\" href=\"javascript:;\" icon=\"icon16_arrow_refresh\"  title=\"重新加载\">刷新</a> "
    sb = sb + "<div class='datagrid-btn-separator'></div> "
    sb = sb + linkbtnTemplate.format("RolePermission", "icon16_molecule", "" if PublicController.IsAuthorized(response, request, "RolePermissionAdmin.Accredit") else "disabled=\"True\"", "角色权限设置", "角色权限")
    sb = sb + linkbtnTemplate.format("RoleUser", "icon16_group_link", "" if PublicController.IsAuthorized(response, request, "RoleManagement.RoleUser") else "disabled=\"True\"", "角色用户关联", "角色用户")
    sb = sb + linkbtnTemplate.format("RoleUserBatchSet", "icon16_folder_user", "" if PublicController.IsAuthorized(response, request, "RoleManagement.RoleUserBatchSet") else "disabled=\"True\"", "角色用户集中批量设置", "角色用户批量设置")
    sb = sb + "<div class='datagrid-btn-separator'></div> "
    sb = sb + linkbtnTemplate.format("RoleBatchPermission", "icon16_shape_square_key", "" if PublicController.IsAuthorized(response, request, "RoleManagement.RoleUserBatchSet") else "disabled=\"True\"", "角色权限集中批量设置", "角色权限批量设置")

    if SystemInfo.EnableUserAuthorizationScope:
        sb = sb + "<a href=\"javascript:void(0)\" id=\"sb\">权限设置</a>"
        sb = sb + GenerateSplitTool()

    sb = sb + "<div class='datagrid-btn-separator'></div> "
    sb = sb + linkbtnTemplate.format("Search", "icon16_filter", "" if PublicController.IsAuthorized(response, request, "UserManagement.Search") else "disabled=\"True\"", "搜索", "搜索")
    return sb


@LoginAuthorize
def Index(request):
    """
    起始页
    Args:
    Returns:
    """
    response = HttpResponse()
    tmp = loader.get_template('RolePermissionAdmin/Index.html')  # 加载模板
    render_content = {'Skin': CommonUtils.Theme(response, request),
                      'ToolButton': BuildToolBarButton(response, request)}  # 将要渲染到模板的数据
    new_body = tmp.render(render_content)  # 渲染模板
    response.content = new_body  # 设置返回内容
    return response