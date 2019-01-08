# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2019/1/8 14:25'

from apps.hadmin.MvcAppUtilties.LoginAuthorize import LoginAuthorize
from apps.hadmin.MvcAppUtilties.CommonUtils import CommonUtils
from apps.hadmin.MvcAppUtilties.PublicController import PublicController
from apps.hadmin.MvcAppUtilties.AjaxOnly import AjaxOnly
from django.http.response import HttpResponse
from django.template import loader ,Context


def GenerateSplitTool():
    sbTool = ''
    sbTool = sbTool + "<div id=\"mm\" style=\"width:100px;\">"
    sbTool = sbTool + "<div id=\"btnLogByUser\" data-options=\"iconCls:'icon16_cheque'\">用户访问详情</div>"
    sbTool = sbTool + "<div id=\"btnLogByGeneral\" data-options=\"iconCls:'icon16_blogs'\">用户访问情况</div>"
    sbTool = sbTool + "</div>"
    return sbTool

def BuildToolBarButton(response, request):
    sb = ''
    linkbtnTemplate = "<a id=\"a_{0}\" class=\"easyui-linkbutton\" style=\"float:left\"  plain=\"true\" href=\"javascript:;\" icon=\"{1}\"  {2} title=\"{3}\">{4}</a>"
    sb = sb + "<a id=\"a_refresh\" class=\"easyui-linkbutton\" style=\"float:left\"  plain=\"true\" href=\"javascript:;\" icon=\"icon16_arrow_refresh\"  title=\"重新加载\">刷新</a> "
    sb = sb + "<div class='datagrid-btn-separator'></div> "
    sb = sb + linkbtnTemplate.format("add", "icon16_user_add", "" if PublicController.IsAuthorized(response, request, "UserManagement.Add") else "disabled=\"True\"", "添加用户", "添加")
    sb = sb + linkbtnTemplate.format("edit", "icon16_user_edit", "" if PublicController.IsAuthorized(response, request, "UserManagement.Edit") else "disabled=\"True\"", "修改用户", "修改")
    sb = sb + linkbtnTemplate.format("delete", "icon16_user_delete", "" if PublicController.IsAuthorized(response, request, "UserManagement.Delete") else "disabled=\"True\"", "删除用户", "删除")
    sb = sb + "<div class='datagrid-btn-separator'></div> "
    sb = sb + linkbtnTemplate.format("editpassword", "icon16_user_level_filtering", "" if PublicController.IsAuthorized(response, request, "UserManagement.SetUserPassword") else "disabled=\"True\"", "设置选中用户密码", "设置密码")
    sb = sb + linkbtnTemplate.format("dimission", "icon16_aol_messenger", "" if PublicController.IsAuthorized(response, request, "UserManagement.Dimission") else "disabled=\"True\"", "离职", "离职")
    sb = sb + "<div class='datagrid-btn-separator'></div> "
    sb = sb + linkbtnTemplate.format("export", "icon16_user_go", "" if PublicController.IsAuthorized(response, request, "UserManagement.Edit") else "disabled=\"True\"", "导出用户数据", "导出")
    sb = sb + "<a href=\"javascript:void(0)\" id=\"sb\">访问日志</a>"
    sb = sb + GenerateSplitTool()
    return sb

@LoginAuthorize
def index(request):
    """
    起始页
    Args:
    Returns:
    """
    response = HttpResponse()
    tmp = loader.get_template('UserAdmin/Index.html')  # 加载模板
    render_content = {'Skin': CommonUtils.Theme(response, request),
                      'CurrentUserId': CommonUtils.Current(response, request).Id,
                      'ToolButton': BuildToolBarButton(response, request)}  # 将要渲染到模板的数据
    new_body = tmp.render(render_content)  # 渲染模板
    response.content = new_body  # 设置返回内容
    return response

@AjaxOnly
@LoginAuthorize
def getuserpagedtbydepartmentid(request):

    

    pass