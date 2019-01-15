# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2019/1/15 13:22'

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
from apps.bizlogic.service.base.MessageService import MessageService
import json
from apps.hadmin.MvcAppUtilties.JsonHelper import DateEncoder

def BuildToolBarButton(response, request):
    sb = ''
    linkbtnTemplate = "<a id=\"a_{0}\" class=\"easyui-linkbutton\" style=\"float:left\"  plain=\"true\" href=\"javascript:;\" icon=\"{1}\"  {2} title=\"{3}\">{4}</a>"
    sb = sb + "<a id=\"a_refresh\" class=\"easyui-linkbutton\" style=\"float:left\"  plain=\"true\" href=\"javascript:;\" icon=\"icon16_arrow_refresh\"  title=\"重新加载\">刷新</a> "
    sb = sb + "<div class='datagrid-btn-separator'></div> "
    sb = sb + linkbtnTemplate.format("sendMessage", "icon16_comment_edit", "" if PublicController.IsAuthorized(response, request, "Resource.ManagePermission") else "disabled=\"True\"", "发送消息", "发消息")
    if CommonUtils.Current(response, request).IsAdministrator:
        sb = sb + linkbtnTemplate.format("broadcastMessage", "icon16_comments_add", "" if PublicController.IsAuthorized(response, request, "Resource.ManagePermission") else "disabled=\"True\"", "广播消息", "广播消息")
    sb = sb + linkbtnTemplate.format("readMessage", "icon16_email_at_sign", "" if PublicController.IsAuthorized(response, request, "Resource.ManagePermission") else "disabled=\"True\"", "标志为已读", "已读")
    sb = sb + "<div class='datagrid-btn-separator'></div> "
    sb = sb + linkbtnTemplate.format("delMessage", "icon16_comment_delete", "" if PublicController.IsAuthorized(response, request, "Resource.ManagePermission") else "disabled=\"True\"", "删除选中的消息", "删除")
    return sb


@LoginAuthorize
def Index(request):
    """
    起始页
    Args:
    Returns:
    """
    response = HttpResponse()
    tmp = loader.get_template('MessageAdmin/Index.html')  # 加载模板
    render_content = {'Skin': CommonUtils.Theme(response, request),
                      'ToolButton': BuildToolBarButton(response, request)}  # 将要渲染到模板的数据
    new_body = tmp.render(render_content)  # 渲染模板
    response.content = new_body  # 设置返回内容
    return response

@LoginAuthorize
def GetMessageListByFunctionCode(request):
    functionCode = None
    searchValue = None
    page = 1
    rows = 20

    try:
        functionCode = request.POST['functionCode']
    except:
        functionCode = None

    try:
        searchValue = request.POST['searchValue']
    except:
        searchValue = ""

    try:
        page = request.POST['page']
    except:
        page = 1

    try:
        rows = request.POST['rows']
    except:
        rows = 20

    response = HttpResponse()
    curUser = CommonUtils.Current(response, request)
    jsons = "[]"
    if functionCode:
        searchValue = searchValue + "functioncode = '" + functionCode + "'"

    if searchValue:
        searchValue = searchValue + " AND "
    else:
        searchValue = ""

    searchValue = searchValue + "((" + 'receiverid' + " = '" + curUser.Id + "' AND " + 'categorycode' + " ='Receiver') " \
                        + " OR  (" +  'createuserid' + " = '" + curUser.Id  + "' AND " + 'categorycode' + " ='Send'))"

    recordCount = 0
    recordCount,dtMessage = MessageService.GetMessagesByConditional(CommonUtils.Current(response, request), searchValue, page, rows)

    messageTmp = ''
    for message in dtMessage:
        messageTmp = messageTmp + ', ' + json.dumps(message, cls=DateEncoder)
        messageTmp = messageTmp.strip(',')
    returnValue = '{"total": ' + str(recordCount) + ', "rows":[' + messageTmp + ']}'
    response.content = returnValue
    return response
