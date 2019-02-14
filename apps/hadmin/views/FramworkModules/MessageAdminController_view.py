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
import json,uuid,datetime
from apps.hadmin.MvcAppUtilties.JsonHelper import DateEncoder
from apps.bizlogic.service.base.UserService import UserSerivce
from apps.bizlogic.models import Cimessage
from apps.utilities.message.FrameworkMessage import FrameworkMessage


def BuildToolBarButton(response, request):
    sb = ''
    linkbtnTemplate = "<a id=\"{0}\" class=\"easyui-linkbutton\" style=\"float:left\"  plain=\"true\" href=\"javascript:;\" icon=\"{1}\"  {2} title=\"{3}\">{4}</a>"
    sb = sb + "<a id=\"refresh\" class=\"easyui-linkbutton\" style=\"float:left\"  plain=\"true\" href=\"javascript:;\" icon=\"icon16_arrow_refresh\"  title=\"重新加载\">刷新</a>"
    sb = sb + "<div class='datagrid-btn-separator'></div> "
    sb = sb + linkbtnTemplate.format("sendMessage", "icon16_comment_edit", "" if PublicController.IsAuthorized(response, request, "MessageAdmin.SendMessage") else "disabled=\"True\"", "发送消息", "发消息")
    if CommonUtils.Current(response, request).IsAdministrator:
        sb = sb + linkbtnTemplate.format("broadcastMessage", "icon16_comments_add", "" if PublicController.IsAuthorized(response, request, "MessageAdmin.BroadcastMessage") else "disabled=\"True\"", "广播消息", "广播消息")
    sb = sb + linkbtnTemplate.format("readMessage", "icon16_email_at_sign", "" if PublicController.IsAuthorized(response, request, "MessageAdmin.ReadMessage") else "disabled=\"True\"", "标志为已读", "已读")
    sb = sb + "<div class='datagrid-btn-separator'></div> "
    sb = sb + linkbtnTemplate.format("delMessage", "icon16_comment_delete", "" if PublicController.IsAuthorized(response, request, "MessageAdmin.DeleteMessage") else "disabled=\"True\"", "删除选中的消息", "删除")
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

@LoginAuthorize
def SendMessageForm(request):
    response = HttpResponse()
    vUser = CommonUtils.Current(response, request)
    tmp = loader.get_template('MessageAdmin/SendMessage.html')  # 加载模板
    render_content = {'Addresser': vUser.UserName + "（" + vUser.RealName + "）",
                      'Skin': CommonUtils.Theme(response, request)}  # 将要渲染到模板的数据
    new_body = tmp.render(render_content)  # 渲染模板
    response.content = new_body  # 设置返回内容
    return response

@LoginAuthorize
def OptionUser(request):
    response = HttpResponse()
    vUser = CommonUtils.Current(response, request)
    tmp = loader.get_template('MessageAdmin/OptionUser.html')  # 加载模板
    render_content = {'Skin': CommonUtils.Theme(response, request)}  # 将要渲染到模板的数据
    new_body = tmp.render(render_content)  # 渲染模板
    response.content = new_body  # 设置返回内容
    return response

@LoginAuthorize
def OptionUserJson(request):
    try:
        keyword = request.GET['keyword']
    except:
        keyword = ''

    response = HttpResponse()
    vUser = CommonUtils.Current(response, request)

    ListData = UserSerivce.Search(vUser, keyword, '', None)
    sb = '['
    if len(ListData) > 0:
        for item in ListData:
            sb = sb + '{'
            sb = sb + "\"id\":\"" + item["ID"] + "\","
            sb = sb + "\"text\":\"" + item["REALNAME"] + "（" + item["USERNAME"] + "）\","
            Genderimg = "user_female"
            if str(item["GENDER"]) == "男":
                Genderimg = "user_green"
            sb = sb + "\"iconCls\":\"icon16_" + Genderimg + "\","
            sb = sb + "\"username\":\"" + item["USERNAME"] + "\","
            sb = sb + "\"code\":\"" + item["CODE"] + "\","
            sb = sb + "\"realname\":\"" + item["REALNAME"] + "\","
            sb = sb + "\"hasChildren\":false"
            sb = sb + "},"
        sb = sb.strip(',')
    sb = sb + ']'
    response.content = sb
    return response

@LoginAuthorize
def SendMessage(request):
    try:
        Title = request.POST['Title']
    except:
        Title = ''

    try:
        MSGContent = request.POST['MSGContent']
    except:
        MSGContent = ''

    try:
        AddresseeJson = request.POST['AddresseeJson']
    except:
        AddresseeJson = '[]'

    response = HttpResponse()
    curUser = CommonUtils.Current(response, request)
    AddressList = json.loads(AddresseeJson)

    message = Cimessage()
    message.id = uuid.uuid4()
    message.title = Title
    message.msgcontent = MSGContent
    message.deletemark = 0
    message.enabled = 1
    message.createon = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    message.createby = curUser.RealName
    message.createuserid = curUser.Id
    message.modifiedby = curUser.RealName
    message.modifieduserid = curUser.Id
    message.modifiedon = message.createon
    message.readcount = 0

    reciveIds = ''

    if AddressList and len(AddressList) > 0:
        for entity in AddressList:
            reciveIds = reciveIds + entity['Id'] + ","
        reciveIds = reciveIds.strip(',')

    if curUser:
        message.modifiedby = curUser.RealName
        message.modifieduserid = curUser.Id

    returnValue = 0
    if reciveIds:
        for id in reciveIds.split(','):
            returnValue = returnValue + MessageService.BatchSend(response, request, id, None, None, message)

    if returnValue > 0:
        response.content = json.dumps({'Success': True, 'Data': '1', 'Message': "发送成功。"})
        return response
    else:
        response.content = json.dumps({'Success': False, 'Data': '0', 'Message': "发送失败。"})
        return response


@LoginAuthorize
def BroadcastMessageForm(request):
    response = HttpResponse()
    vUser = CommonUtils.Current(response, request)
    tmp = loader.get_template('MessageAdmin/BroadcastMessage.html')  # 加载模板
    render_content = {'Addresser': vUser.UserName + "（" + vUser.RealName + "）",
                      'Skin': CommonUtils.Theme(response, request)}  # 将要渲染到模板的数据
    new_body = tmp.render(render_content)  # 渲染模板
    response.content = new_body  # 设置返回内容
    return response

@LoginAuthorize
def BroadcastMessage(request):
    try:
        message = request.POST['message']
    except:
        message = ''

    response = HttpResponse()
    if message:
        returnValue = MessageService.Broadcast(response, request, message)
    if returnValue > 0:
        response.content = json.dumps({'Success': True, 'Data': '1', 'Message': "发送成功。"})
        return response
    else:
        response.content = json.dumps({'Success': False, 'Data': '0', 'Message': "发送失败。"})
        return response

@LoginAuthorize
def ReadMessage(request):
    try:
        key = request.POST['key']
    except:
        key = ''
    returnValue = 0
    response = HttpResponse()
    curUser = CommonUtils.Current(response, request)

    if key:
        returnValue = MessageService.Read(curUser, key)

    if returnValue > 0:
        response.content = json.dumps({'Success': True, 'Data': '1', 'Message': FrameworkMessage.MSG3010})
        return response
    else:
        response.content = json.dumps({'Success': False, 'Data': '0', 'Message': FrameworkMessage.MSG3020})
        return response


@LoginAuthorize
def Delete(request):
    try:
        key = request.POST['key']
    except:
        key = ''
    response = HttpResponse()
    returnValue = 0
    if key:
        returnValue = MessageService.SetDeleted(CommonUtils.Current(response, request), [key])

    if returnValue > 0:
        response.content = json.dumps({'Success': True, 'Data': '1', 'Message': FrameworkMessage.MSG3010})
        return response
    else:
        response.content = json.dumps({'Success': False, 'Data': '0', 'Message': FrameworkMessage.MSG3020})
        return response

