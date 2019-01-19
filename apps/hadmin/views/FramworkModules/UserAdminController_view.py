# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2019/1/8 14:25'

from apps.hadmin.MvcAppUtilties.LoginAuthorize import LoginAuthorize
from apps.hadmin.MvcAppUtilties.CommonUtils import CommonUtils
from apps.hadmin.MvcAppUtilties.PublicController import PublicController
from apps.hadmin.MvcAppUtilties.AjaxOnly import AjaxOnly
from apps.hadmin.MvcAppUtilties.JsonHelper import DateEncoder
from django.http.response import HttpResponse
from django.http import JsonResponse
from django.template import loader ,Context
from apps.bizlogic.service.base.UserOrganizeSerivce import UserOrganizeService
from apps.bizlogic.service.base.UserService import UserSerivce
import json
from apps.utilities.publiclibrary.SearchFilter import SearchFilter
from apps.bizlogic.models import Piuser
from apps.utilities.message.StatusCode import StatusCode
from apps.utilities.message.FrameworkMessage import FrameworkMessage
import uuid
import datetime

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
def Index(request):
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


@LoginAuthorize
def Form(request):
    """
    起始页
    Args:
    Returns:
    """
    response = HttpResponse()
    tmp = loader.get_template('UserAdmin/Form.html')  # 加载模板
    render_content = {}  # 将要渲染到模板的数据
    new_body = tmp.render(render_content)  # 渲染模板
    response.content = new_body  # 设置返回内容
    return response

@AjaxOnly
@LoginAuthorize
def GetUserPageDTByDepartmentId(request):

    organizeId = None
    try:
        organizeId = request.POST['organizeId']
    except:
        organizeId = None

    try:
        searchValue = request.POST['searchValue']
    except:
        searchValue = ''

    try:
        page = request.POST['page']
    except:
        page = 1

    try:
        rows = request.POST['rows']
    except:
        rwos = 20

    searchValue = searchValue if searchValue else ''

    response = HttpResponse()
    jsons = "[]"
    returnValue = ''

    if organizeId:
        recordCount = 0
        recordCount,dtUser = UserOrganizeService.GetUserPageDTByDepartment(None, CommonUtils.Current(response, request), 'Resource.ManagePermission', searchValue, None, '', None,  True, True, page, rows, 'sortcode', organizeId)
        userTmp = ''
        for user in dtUser:
            userTmp = userTmp + ', ' + json.dumps(user, cls=DateEncoder)
        userTmp = userTmp.strip(',')
        returnValue = '{"total": '+ str(recordCount) +', "rows":['+ userTmp +']}'
        response.content = returnValue
    else:
        response.content = jsons

    return response

@AjaxOnly
@LoginAuthorize
def GetUserListByPage(request):
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
        rows = 50

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
    dtUser = UserSerivce.GetDTByPage(None, SearchFilter.TransfromFilterToSql(filter, False), '', '', rows, sort + ' ' + order)

    recordCount = dtUser.count
    pageValue = dtUser.page(page)

    userTmp = ''
    for role in pageValue:
        userTmp = userTmp + ', ' + json.dumps(role, cls=DateEncoder)
        userTmp = userTmp.strip(',')
    returnValue = '{"total": ' + str(recordCount) + ', "rows":[' + userTmp + ']}'

    response.content = returnValue
    return response

@LoginAuthorize
def SubmitForm(request):
    try:
        IsOk = '1'
        try:
            key = request.GET['key']
        except:
            key = None

        response = HttpResponse()

        curUser = CommonUtils.Current(response, request)

        if not key:
            user = Piuser()
            user = user.loadJson(request)
            user.id = uuid.uuid4()
            # user.isstaff = 0
            # user.isvisible = 1
            # user.isdimission = 0
            user.deletemark = 0
            user.createon = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            user.createby = curUser.RealName
            user.createuserid = curUser.Id
            user.isstaff = 0
            user.isvisible = 1
            user.isdimission = 0


            returnCode, returnMessage, returnValue = UserSerivce.AddUser(None, user)
            if returnCode == StatusCode.statusCodeDic['OKAdd']:
                response.content = json.dumps({'Success':True, 'Data':IsOk, 'Message':returnMessage})
                return response
            else:
                response.content = json.dumps({'Success': False, 'Data': '0', 'Message': returnMessage})
                return response
        else:
            updateEntity = UserSerivce.GetEntity(key)
            if updateEntity:
                updateEntity = updateEntity.loadJson(request)

            if curUser:
                updateEntity.modifiedby = curUser.RealName
                updateEntity.modifieduserid = curUser.Id
                returnCode, returnMessage = UserSerivce.UpdateUser(None, updateEntity)
                if returnCode == StatusCode.statusCodeDic['OKUpdate']:
                    response.content = json.dumps({'Success': True, 'Data': IsOk, 'Message': returnMessage})
                    return response
                else:
                    response.content = json.dumps({'Success': False, 'Data': '0', 'Message': returnMessage})
                    return response
    except Exception as e:
        print(e)
        response = HttpResponse()
        response.content = json.dumps({'Success': False, 'Data': '0', 'Message': FrameworkMessage.MSG3020})
        return response

@LoginAuthorize
def GetEntity(request):
    try:
        key = request.POST['key']
    except:
        key = None
    entity = UserSerivce.GetEntity(key)
    response = HttpResponse()
    response.content = entity.toJSON()
    return response

@LoginAuthorize
def Delete(request):
    try:
        key = request.POST['key']
    except:
        key = ''

    returnValue = UserSerivce.SetDeleted(None, [key])

    if returnValue:
        response = HttpResponse()
        response.content = json.dumps({'Success': True, 'Data': '1', 'Message': FrameworkMessage.MSG0013})
        return response
    else:
        response = HttpResponse()
        response.content = json.dumps({'Success': False, 'Data': '0', 'Message': FrameworkMessage.MSG3020})
        return response
