# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2019/1/11 14:07'

from django.template import loader ,Context
from apps.hadmin.MvcAppUtilties.PublicController import PublicController
from apps.hadmin.MvcAppUtilties.LoginAuthorize import LoginAuthorize
from django.http.response import HttpResponse
from apps.hadmin.MvcAppUtilties.CommonUtils import CommonUtils

def BuildToolBarButton(response, request):
    sb = ''
    linkbtnTemplate = "<a id=\"a_{0}\" class=\"easyui-linkbutton\" style=\"float:left\"  plain=\"true\" href=\"javascript:;\" icon=\"{1}\"  {2} title=\"{3}\">{4}</a>"
    sb = sb + "<a id=\"a_refresh\" class=\"easyui-linkbutton\" style=\"float:left\"  plain=\"true\" href=\"javascript:;\" icon=\"icon16_arrow_refresh\"  title=\"重新加载\">刷新</a> "
    sb = sb + "<div class='datagrid-btn-separator'></div> "
    sb = sb + linkbtnTemplate.format("add", "icon16_brick_add", "" if PublicController.IsAuthorized(response, request, "PostAdmin.Add") else "disabled=\"True\"", "添加岗位", "添加")
    sb = sb + linkbtnTemplate.format("edit", "icon16_brick_edit", "" if PublicController.IsAuthorized(response, request, "PostAdmin.Edit") else "disabled=\"True\"", "修改岗位", "修改")
    sb = sb + linkbtnTemplate.format("delete", "icon16_brick_delete", "" if PublicController.IsAuthorized(response, request, "PostAdmin.Delete") else "disabled=\"True\"", "删除岗位", "删除")
    sb = sb + "<div class='datagrid-btn-separator'></div> "
    sb = sb + linkbtnTemplate.format("moveTo", "icon16_arrow_switch", "" if PublicController.IsAuthorized(response, request, "PostAdmin.Edit") else "disabled=\"True\"", "移动选中的岗位", "移动")
    sb = sb + "<div class='datagrid-btn-separator'></div> "
    sb = sb + linkbtnTemplate.format("setUser", "icon16_key", "" if PublicController.IsAuthorized(response, request, "PostAdmin.User") else "disabled=\"True\"", "设置选中岗位所包含的用户", "设置用户")
    sb = sb + linkbtnTemplate.format("setPermission", "icon16_lightning", "" if PublicController.IsAuthorized(response, request, "PostAdmin.Permission") else "disabled=\"True\"", "设置选中岗位所拥有的权限", "设置权限")
    return sb

@LoginAuthorize
def Index(request):
    """
        起始页
        Args:
        Returns:
        """
    response = HttpResponse()
    tmp = loader.get_template('PostAdmin/Index.html')  # 加载模板
    render_content = {'Skin': CommonUtils.Theme(response, request),
                      'ToolButton': BuildToolBarButton(response, request)}  # 将要渲染到模板的数据
    new_body = tmp.render(render_content)  # 渲染模板
    response.content = new_body  # 设置返回内容
    return response

