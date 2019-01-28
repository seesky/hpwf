# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2019/1/10 14:33'

from apps.hadmin.MvcAppUtilties.LoginAuthorize import LoginAuthorize
from django.http.response import HttpResponse
from django.template import loader ,Context
from apps.hadmin.MvcAppUtilties.CommonUtils import CommonUtils
from apps.hadmin.MvcAppUtilties.PublicController import PublicController
from apps.hadmin.MvcAppUtilties.AjaxOnly import AjaxOnly
from apps.bizlogic.service.base.RoleService import RoleService
from apps.utilities.publiclibrary.SearchFilter import SearchFilter
from apps.utilities.publiclibrary.SystemInfo import SystemInfo
import json
from apps.hadmin.MvcAppUtilties.JsonHelper import DateEncoder
from apps.bizlogic.service.base.ItemDetailsService import ItemDetailsService
from apps.bizlogic.service.base.RoleService import RoleService
from apps.bizlogic.service.permission.ScopPermission import ScopPermission
from apps.bizlogic.models import Pirole
import datetime
from apps.utilities.message.StatusCode import StatusCode
from apps.utilities.message.FrameworkMessage import FrameworkMessage
import uuid
from apps.bizlogic.service.base.UserRoleService import UserRoleService

def BuildToolBarButton(response, request):
    sb = ''
    linkbtnTemplate = "<a id=\"a_{0}\" class=\"easyui-linkbutton\" style=\"float:left\"  plain=\"true\" href=\"javascript:;\" icon=\"{1}\"  {2} title=\"{3}\">{4}</a>"
    sb = sb + "<a id=\"a_refresh\" class=\"easyui-linkbutton\" style=\"float:left\"  plain=\"true\" href=\"javascript:;\" icon=\"icon16_arrow_refresh\"  title=\"重新加载\">刷新</a> "
    sb = sb + "<div class='datagrid-btn-separator'></div> "
    sb = sb + linkbtnTemplate.format("add", "icon16_group_add", "" if PublicController.IsAuthorized(response, request, "RoleManagement.Add") else "disabled=\"True\"", "新增角色", "新增")
    sb = sb + linkbtnTemplate.format("edit", "icon16_group_edit", "" if PublicController.IsAuthorized(response, request, "RoleManagement.Edit") else "disabled=\"True\"", "修改选中角色", "修改")
    sb = sb + linkbtnTemplate.format("del", "icon16_group_delete", "" if PublicController.IsAuthorized(response, request, "RoleManagement.Delete") else "disabled=\"True\"", "删除选中角色", "删除")
    sb = sb + "<div class='datagrid-btn-separator'></div> "
    sb = sb + linkbtnTemplate.format("roleuser", "icon16_group_link", "" if PublicController.IsAuthorized(response, request, "RoleManagement.RoleUser") else "disabled=\"True\"", "设置当前角色拥有的用户", "角色用户设置")
    sb = sb + "<div class='datagrid-btn-separator'></div> "
    sb = sb + linkbtnTemplate.format("export", "icon16_group_go", "" if PublicController.IsAuthorized(response, request, "RoleManagement.Export") else "disabled=\"True\"", "导出角色数据", "导出")
    sb = sb + linkbtnTemplate.format("print", "icon16_printer", "" if PublicController.IsAuthorized(response, request, "RoleManagement.Export") else "disabled=\"True\"", "打印", "打印")
    return sb


@LoginAuthorize
def Index(request):
    """
    起始页
    Args:
    Returns:
    """
    response = HttpResponse()
    tmp = loader.get_template('RoleAdmin/Index.html')  # 加载模板
    render_content = {'Skin': CommonUtils.Theme(response, request),
                      'ToolButton': BuildToolBarButton(response, request)}  # 将要渲染到模板的数据
    new_body = tmp.render(render_content)  # 渲染模板
    response.content = new_body  # 设置返回内容
    return response

@LoginAuthorize
def GridPageListJson(request):
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
        rows = 20

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
    dtRole = RoleService.GetDtByPage(None, rows, SearchFilter.TransfromFilterToSql(filter, False), sort + ' ' + order)
    recordCount = dtRole.count
    pageValue = dtRole.page(page)

    roleTmp = ''
    for role in pageValue:
        roleTmp = roleTmp + ', ' + json.dumps(role, cls=DateEncoder)
    roleTmp = roleTmp.strip(',')
    returnValue = '{"total": ' + str(recordCount) + ', "rows":[' + roleTmp + ']}'

    response.content = returnValue
    return response

@LoginAuthorize
def GetRoleCategory(request):
    categoryCode = None
    try:
        categoryCode = request.GET['categoryCode']
    except:
        categoryCode = None

    response = HttpResponse()
    dtItemDetail = ItemDetailsService.GetDTByCode(None, categoryCode)

    jsons = ''
    jsons = jsons + '['
    jsons = jsons + '{"ITEMCODE": null,"ITEMNAME": "==选择所有分类==","ITEMVALUE": "0"},'
    for item in dtItemDetail:
        jsons = jsons + '{"ITEMCODE": "' + item.itemcode + '","ITEMNAME": "' + item.itemname + '","ITEMVALUE": "' + item.itemvalue + '"},'
    jsons = jsons.strip(',')
    jsons = jsons + ']'
    response.content = jsons
    return response

@LoginAuthorize
def GetRoleListByOrganize(request):
    organizeId = None
    try:
        organizeId = request.POST['organizeId']
    except:
        organizeId = None

    response = HttpResponse()
    writeJson = "[]"
    tempJson = "["
    if organizeId:
        roles = RoleService.GetDTByOrganize(None, organizeId, True)
        for role in roles:
            tempJson = tempJson + str(role.toJSON()) + ","
        tempJson = tempJson.strip(",")
        tempJson = tempJson + "]"
        response.content = tempJson
        return response
    else:
        response.content = writeJson
        return response

@LoginAuthorize
def GetEnabledRoleList(request):
    returnValue = "[]"
    dtRole = RoleService.GetDTByValues(None, {'deletemark':0, 'enabled':1})
    if dtRole and len(dtRole) > 0:
        returnValue = '['
        for role in dtRole:
            returnValue = returnValue + role.toJSON() + ","
        returnValue = returnValue.strip(",")
        returnValue = returnValue + "]"

        response = HttpResponse()
        response.content = returnValue
        return response

    return returnValue


@LoginAuthorize
def Form(request):
    """
    起始页
    Args:
    Returns:
    """
    response = HttpResponse()
    tmp = loader.get_template('RoleAdmin/Form.html')  # 加载模板
    render_content = {}  # 将要渲染到模板的数据
    new_body = tmp.render(render_content)  # 渲染模板
    response.content = new_body  # 设置返回内容
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
            role = Pirole()
            role = role.loadJson(request)

            role.id = uuid.uuid4()
            # user.isstaff = 0
            # user.isvisible = 1
            # user.isdimission = 0
            role.deletemark = 0
            role.allowdelete = 1
            role.allowedit = 1
            role.createon = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            role.createby = curUser.RealName
            role.modifiedon = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            role.modifiedby = curUser.RealName
            role.enabled = 1

            returnCode, returnMessage, returnValue = RoleService.Add(None, role)


            if returnCode == StatusCode.statusCodeDic['OKAdd']:
                response.content = json.dumps({'Success':True, 'Data':IsOk, 'Message':returnMessage})
                return response
            else:
                response.content = json.dumps({'Success': False, 'Data': '0', 'Message': returnMessage})
                return response
        else:
            role = RoleService.GetEntity(None, key)
            if role:
                role = role.loadJson(request)

            if curUser:
                role.modifiedby = curUser.RealName
                role.modifieduserid = curUser.Id
                returnCode, returnMessage = RoleService.Update(None, role)
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
    entity = RoleService.GetEntity(None, key)
    response = HttpResponse()
    response.content = entity.toJSON()
    return response

@LoginAuthorize
def Delete(request):
    try:
        key = request.POST['key']
    except:
        key = ''

    returnValue = RoleService.SetDeleted(None, [key])

    if returnValue:
        response = HttpResponse()
        response.content = json.dumps({'Success': True, 'Data': '1', 'Message': FrameworkMessage.MSG0013})
        return response
    else:
        response = HttpResponse()
        response.content = json.dumps({'Success': False, 'Data': '0', 'Message': FrameworkMessage.MSG3020})
        return response

@LoginAuthorize
def AddUserToRole(request):
    try:
        roleId = request.POST['roleId']
        addUserIds = request.POST['addUserIds']
    except:
        roleId = None
        addUserIds = None

    response = HttpResponse()
    if roleId and len(str(addUserIds).strip()) > 0:
        returnValue = RoleService.AddUserToRole(CommonUtils.Current(response, request), roleId, str(addUserIds).split(','))
        if returnValue > 0:
            response.content = json.dumps({'Success': True, 'Data': '1', 'Message': '添加成功！'})
            return response
        else:
            response.content = json.dumps({'Success': False, 'Data': '0', 'Message': '添加失败！'})
            return response
    else:
        response = HttpResponse()
        response.content = json.dumps({'Success': False, 'Data': '0', 'Message': '无选择的用户！'})
        return response

@LoginAuthorize
def RemoveUserFromRole(request):
    try:
        roleId = request.POST['roleId']
        userId = request.POST['userId']
    except:
        roleId = None
        userId = None

    response = HttpResponse()
    if not userId:
        response.content = json.dumps({'Success': False, 'Data': '0', 'Message': '无选择的用户！'})
        return response
    else:
        returnValue = RoleService.RemoveUserFromRole(CommonUtils.Current(response, request), [userId], roleId)
        if returnValue > 0:
            response.content = json.dumps({'Success': True, 'Data': '1', 'Message': FrameworkMessage.MSG3010})
            return response
        else:
            response.content = json.dumps({'Success': False, 'Data': '0', 'Message': FrameworkMessage.MSG3020})
            return response

def GetRoleScope(userInfo, permissionItemScopeCode):
    if userInfo.IsAdministrator or (not permissionItemScopeCode) or (not SystemInfo.EnableUserAuthorizationScope):
        returnValue = RoleService.GetDT(None)
    else:
        returnValue = ScopPermission.GetRoleDTByPermissionScope(userInfo, permissionItemScopeCode)
    return returnValue

@LoginAuthorize
def GetRoleList(request):
    response = HttpResponse()
    roleDT = GetRoleScope(CommonUtils.Current(response, request), "Resource.ManagePermission")
    returnValue = '['
    for role in roleDT:
        returnValue = returnValue + role.toJSON() + ","
    returnValue = returnValue.strip(",")
    returnValue = returnValue + "]"
    response.content = returnValue
    return response

def GetRoleListByUserId(request):
    try:
        userId = request.GET['userId']
    except:
        userId = None

    response = HttpResponse()
    if userId:
        roleIds = UserRoleService.GetUserRoleIds(None, userId)

    jsons = '[]'
    if roleIds and len(roleIds) > 0:
        roleDT = RoleService.GetDTByIds(None, roleIds)
        returnValue = '['
        for role in roleDT:
            returnValue = returnValue + role.toJSON() + ","
        returnValue = returnValue.strip(",")
        returnValue = returnValue + "]"
        response.content = returnValue
        return response
    else:
        response.content = jsons
        return response