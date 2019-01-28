# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2019/1/14 9:45'

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
    sbTool = sbTool + "<div id=\"btnUserPermissionScope\" data-options=\"iconCls:'icon16_report_user'\">用户授权范围</div>"
    sbTool = sbTool + "<div id=\"btnUserTableFieldPermission\" data-options=\"iconCls:'icon16_timeline_marker'\">表字段权限设置</div>"
    sbTool = sbTool + "<div id=\"btnUserTableConstraintSet\"  data-options=\"iconCls:'icon16_script_key'\">约束条件权限设置</div>"
    sbTool = sbTool + "</div>"
    return sbTool

def BuildToolBarButton(response, request):
    sb = ''
    linkbtnTemplate = "<a id=\"btn{0}\" class=\"easyui-linkbutton\" style=\"float:left\"  plain=\"true\" href=\"javascript:;\" icon=\"{1}\"  {2} title=\"{3}\">{4}</a>"
    sb = sb + "<a id=\"a_refresh\" class=\"easyui-linkbutton\" style=\"float:left\"  plain=\"true\" href=\"javascript:;\" icon=\"icon16_arrow_refresh\"  title=\"重新加载\">刷新</a> "
    sb = sb + "<div class='datagrid-btn-separator'></div> "
    sb = sb + linkbtnTemplate.format("UserPermission", "icon16_key", "" if PublicController.IsAuthorized(response, request, "UserPermissionAdmin.UserPermission") else "disabled=\"True\"", "用户权限设置", "用户权限")
    sb = sb + linkbtnTemplate.format("UserRole", "icon16_group_link", "" if PublicController.IsAuthorized(response, request, "UserPermissionAdmin.UserRole") else "disabled=\"True\"", "用户角色关联", "用户角色")
    sb = sb + linkbtnTemplate.format("UserRoleBatchSet", "icon16_shape_square_key", "" if PublicController.IsAuthorized(response, request, "UserPermissionAdmin.RoleUserBatchSet") else "disabled=\"True\"", "用户角色集中批量设置", "用户角色批量设置")
    sb = sb + "<div class='datagrid-btn-separator'></div> "
    sb = sb + linkbtnTemplate.format("UserBatchPermission", "icon16_lightning", "" if PublicController.IsAuthorized(response, request, "UserPermissionAdmin.BatchPermission") else "disabled=\"True\"", "用户权限集中批量设置", "用户权限批量设置")

    if PublicController.IsAuthorized(response, request, "UserPermissionAdmin.UserAuthorization") and SystemInfo.EnableUserAuthorizationScope:
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
    tmp = loader.get_template('UserPermissionAdmin/Index.html')  # 加载模板
    render_content = {'Skin': CommonUtils.Theme(response, request),
                      'ToolButton': BuildToolBarButton(response, request)}  # 将要渲染到模板的数据
    new_body = tmp.render(render_content)  # 渲染模板
    response.content = new_body  # 设置返回内容
    return response