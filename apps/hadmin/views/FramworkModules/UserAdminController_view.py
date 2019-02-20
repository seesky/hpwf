# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2019/1/8 14:25'

from apps.hadmin.MvcAppUtilties.LoginAuthorize import LoginAuthorize
from apps.hadmin.MvcAppUtilties.IsAuthorized import IsAuthorized
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
from apps.bizlogic.service.base.LogOnService import LogOnService
from apps.utilities.publiclibrary.SystemInfo import SystemInfo
from apps.bizlogic.service.permission.ScopPermission import ScopPermission
from apps.bizlogic.service.base.UserRoleService import UserRoleService
from apps.bizlogic.service.base.SequenceService import SequenceService


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
@IsAuthorized('UserManagement.Edit')
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
    dtUser = UserSerivce.GetDTByPage(CommonUtils.Current(response, request), SearchFilter.TransfromFilterToSql(filter, False), '', '', rows, sort + ' ' + order)

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
@IsAuthorized('UserManagement.Edit')
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
            if user.sortcode == None or user.sortcode == 0:
                sequence = SequenceService.GetSequence(None, 'PIUSER')
                user.sortcode = int(sequence)


            returnCode, returnMessage, returnValue = UserSerivce.AddUser(CommonUtils.Current(response, request), user)
            if returnCode == StatusCode.statusCodeDic['OKAdd']:
                response.content = json.dumps({'Success':True, 'Data':IsOk, 'Message':returnMessage})
                return response
            else:
                response.content = json.dumps({'Success': False, 'Data': '0', 'Message': returnMessage})
                return response
        else:
            updateEntity = UserSerivce.GetEntity(CommonUtils.Current(HttpResponse(), request), key)
            if updateEntity:
                updateEntity = updateEntity.loadJson(request)

            if curUser:
                updateEntity.modifiedby = curUser.RealName
                updateEntity.modifieduserid = curUser.Id
                returnCode, returnMessage = UserSerivce.UpdateUser(CommonUtils.Current(response, request), updateEntity)
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
    entity = UserSerivce.GetEntity(CommonUtils.Current(HttpResponse(), request), key)
    response = HttpResponse()
    response.content = entity.toJSON()
    return response

@LoginAuthorize
@IsAuthorized('UserManagement.Delete')
def Delete(request):
    try:
        key = request.POST['key']
    except:
        key = ''

    returnValue = UserSerivce.SetDeleted(CommonUtils.Current(HttpResponse(), request), [key])

    if returnValue:
        response = HttpResponse()
        response.content = json.dumps({'Success': True, 'Data': '1', 'Message': FrameworkMessage.MSG0013})
        return response
    else:
        response = HttpResponse()
        response.content = json.dumps({'Success': False, 'Data': '0', 'Message': FrameworkMessage.MSG3020})
        return response

@LoginAuthorize
def SetUserPassword(request):
    userId = ''
    password = ''
    try:
        userId = request.POST['userId']
    except:
        userId = ''

    try:
        password = request.POST['password']
    except:
        password = ''

    if userId and password:
        returnCode, returnValue = LogOnService.SetPassword(None, [userId], password)
        if returnCode and returnCode == StatusCode.statusCodeDic['SetPasswordOK']:
            response = HttpResponse()
            response.content = json.dumps({'Success': True, 'Data': '1', 'Message': FrameworkMessage.MSG9963})
            return response
        else:
            response = HttpResponse()
            response.content = json.dumps({'Success': True, 'Data': '1', 'Message': FrameworkMessage.MSG3020})
            return response

@LoginAuthorize
def UserDimission(request):
    #TODO:用户离职的所有前台代码需要重写
    response = HttpResponse()
    tmp = loader.get_template('UserAdmin/UserDimission.html')  # 加载模板
    render_content = {}  # 将要渲染到模板的数据
    new_body = tmp.render(render_content)  # 渲染模板
    response.content = new_body  # 设置返回内容
    return response

@LoginAuthorize
def SetUserDimission(request):
    response = HttpResponse()
    curUser = CommonUtils.Current(response, request)
    userEntity = Piuser()
    userEntity.loadJson(request)
    if userEntity.username and userEntity.id:
        userEntity.username = UserSerivce.GetEntity(curUser.Id).username
    returnValue = LogOnService.UserDimission(None, userEntity.username, userEntity.dimissioncause, userEntity.dimissiondate, userEntity.dimissionwhither)

    if returnValue > 0:
        response = HttpResponse()
        response.content = json.dumps({'Success': True, 'Data': '1', 'Message': FrameworkMessage.MSG3010})
        return response
    else:
        response = HttpResponse()
        response.content = json.dumps({'Success': False, 'Data': '0', 'Message': FrameworkMessage.MSG3020})
        return response

@LoginAuthorize
def GetUserListJson(request):
    response = HttpResponse()
    user = CommonUtils.Current(response, request)
    if user.IsAdministrator or (not "Resource.ManagePermission") or (SystemInfo.EnableUserAuthorizationScope):
        dtUser = UserSerivce.GetDT(user)
    else:
        dtUser = ScopPermission.GetUserDTByPermissionScope(None, user.Id, "Resource.ManagePermission")

    userTmp = ''
    for user in dtUser:
        userTmp = userTmp + ', ' + user.toJSON()
    userTmp = userTmp.strip(',')
    returnValue = '[' + userTmp + ']'
    response.content = returnValue
    return response

@LoginAuthorize
def GetDTByRole(request):
    try:
        roleId = request.GET['roleId']
    except:
        roleId = ''

    jsons = "[]"

    if roleId:
        roleDT = UserRoleService.GetDTByRole(None, roleId)
        userTmp = ''
        for user in roleDT:
            userTmp = userTmp + ', ' + user.toJSON()
        userTmp = userTmp.strip(',')
        returnValue = '[' + userTmp + ']'
        response = HttpResponse()
        response.content = returnValue
        return response
    else:
        response = HttpResponse()
        response.content = jsons
        return response

def RemoveRoleByUserId(request):
    try:
        userId = request.POST['userId']
    except:
        userId = None

    try:
        removeRoleIds = request.POST['targetIds']
    except:
        removeRoleIds = None

    if removeRoleIds and len(removeRoleIds) > 0 and userId:
        returnValue = UserRoleService.RemoveUserFromRole(None, userId, removeRoleIds)
        if returnValue > 0:
            response = HttpResponse()
            response.content = json.dumps({'Success': True, 'Data': '1', 'Message': FrameworkMessage.MSG3010})
            return response
        else:
            response = HttpResponse()
            response.content = json.dumps({'Success': True, 'Data': '0', 'Message': FrameworkMessage.MSG3020})
            return response
    else:
        response = HttpResponse()
        response.content = json.dumps({'Success': False, 'Data': '0', 'Message': FrameworkMessage.MSG3020})
        return response