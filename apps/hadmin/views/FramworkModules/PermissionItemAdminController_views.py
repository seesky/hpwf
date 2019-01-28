# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2019/1/14 7:56'

from apps.hadmin.MvcAppUtilties.CommonUtils import CommonUtils
from apps.hadmin.MvcAppUtilties.PublicController import PublicController
from apps.hadmin.MvcAppUtilties.LoginAuthorize import LoginAuthorize
from apps.hadmin.MvcAppUtilties.AjaxOnly import AjaxOnly
from apps.utilities.publiclibrary.SystemInfo import SystemInfo
from apps.utilities.message.StatusCode import StatusCode
from apps.utilities.message.FrameworkMessage import FrameworkMessage
from apps.bizlogic.models import Pipermissionitem
from apps.bizlogic.service.base.PermissionItemService import PermissionItemService
from apps.bizlogic.service.permission.ScopPermission import ScopPermission
from django.http.response import HttpResponse
from django.template import loader ,Context
from django.db.models import Q
import json,datetime,uuid


def BuildToolBarButton(response, request):
    sb = ''
    linkbtnTemplate = "<a id=\"a_{0}\" class=\"easyui-linkbutton\" style=\"float:left\"  plain=\"true\" href=\"javascript:;\" icon=\"{1}\"  {2} title=\"{3}\">{4}</a>"
    sb = sb + "<a id=\"a_refresh\" class=\"easyui-linkbutton\" style=\"float:left\"  plain=\"true\" href=\"javascript:;\" icon=\"icon16_arrow_refresh\"  title=\"重新加载\">刷新</a> "
    sb = sb + "<div class='datagrid-btn-separator'></div> "
    sb = sb + linkbtnTemplate.format("add", "icon16_layout_add", "" if PublicController.IsAuthorized(response, request, "PermissionItemManagement.Add") else "disabled=\"True\"", "新增操作权限", "新增")
    sb = sb + linkbtnTemplate.format("edit", "icon16_layout_edit", "" if PublicController.IsAuthorized(response, request, "PermissionItemManagement.Edit") else "disabled=\"True\"", "修改操作权限", "修改")
    sb = sb + linkbtnTemplate.format("delete", "icon16_layout_delete", "" if PublicController.IsAuthorized(response, request, "PermissionItemManagement.Delete") else "disabled=\"True\"", "删除操作权限", "删除")
    sb = sb + "<div class='datagrid-btn-separator'></div> "
    sb = sb + linkbtnTemplate.format("move", "icon16_arrow_switch", "" if PublicController.IsAuthorized(response, request, "PermissionItemManagement.Move") else "disabled=\"True\"", "移动选中的操作权限", "移动")
    #sb = sb + linkbtnTemplate.format("export", "icon16_export_excel", "" if PublicController.IsAuthorized(response, request,  "PermissionItemManagement.Export") else "disabled=\"True\"", "导出操作权限列表", "导出")
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

def GetPermissionItemScop(response, request, permissionItemScopeCode):
    vUser = CommonUtils.Current(response, request)

    if vUser.IsAdministrator or (not permissionItemScopeCode) or (SystemInfo.EnableUserAuthorizationScope):
        dtPermissionItem = PermissionItemService.GetDT(None)
    else:
        dtPermissionItem = ScopPermission.GetPermissionItemDTByPermissionScope(None, vUser.Id, permissionItemScopeCode)
    return dtPermissionItem

def GroupJsondata(groups, parentId):
    treeLevel = 0
    sb = ""
    list = []
    for g in groups:
        if g.parentid == parentId:
            list.append(g)
    for g in list:
        treeLevel = treeLevel + 1
        jsons = g.toJSON()
        jsons = jsons.rstrip('}')
        sb = sb + jsons

        sb = sb + ","

        if treeLevel >= 2 and len(groups.filter(Q(parentid=g.id))) > 0:
            sb = sb + "\"state\":\"closed\","

        sb = sb + "\"children\":["

        if g.id:
            sb = sb + GroupJsondata(groups, g.id)
        sb = sb + "]},"
    sb = sb.rstrip(',')
    return sb

@LoginAuthorize
@AjaxOnly
def GetPermissionItemTreeJson(request):
    isTree = None
    try:
        isTree = request.GET['isTree']
        if isTree == '1':
            isTree = True
        else:
            isTree = False
    except:
        isTree = False

    response = HttpResponse()
    dtPermissionItem = GetPermissionItemScop(response, request, 'Resource.ManagePermission')
    CommonUtils.CheckTreeParentId(dtPermissionItem, 'id', 'parentid')
    itemJson = "[" + GroupJsondata(dtPermissionItem, "#") + "]"
    if isTree:
        response.content = itemJson.replace('fullname', "text")
        return response
    else:
        response.content = itemJson
        return response


def GetJsonData(dtPermissionItem):
    CommonUtils.CheckTreeParentId(dtPermissionItem, 'id', 'parentid')
    if dtPermissionItem and dtPermissionItem.count() > 0:
        return "[" + GroupJsondata(dtPermissionItem, "#") + "]"

def GetPermissionItemByIds(request):
    permissionItemIds = None
    try:
        permissionItemIds = request.POST['permissionItemIds']
    except:
        permissionItemIds = None
    response = HttpResponse()
    dtPermissionItem = PermissionItemService.GetDTByIds(None, str(permissionItemIds).split(','))
    treeData = GetJsonData(dtPermissionItem)
    response.content = treeData
    return response

@LoginAuthorize
def Form(request):
    response = HttpResponse()
    tmp = loader.get_template('PermissionItemAdmin/Form.html')  # 加载模板
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
            item = Pipermissionitem()
            item = item.loadJson(request)

            item.id = uuid.uuid4()
            # user.isstaff = 0
            # user.isvisible = 1
            # user.isdimission = 0
            item.deletemark = 0
            item.createon = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            item.createby = curUser.RealName
            item.createuserid = curUser.Id
            item.modifiedon = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            item.modifiedby = curUser.RealName
            item.enabled = 1

            returnCode, returnMessage, returnValue = PermissionItemService.Add(None, item)


            if returnCode == StatusCode.statusCodeDic['OKAdd']:
                response.content = json.dumps({'Success':True, 'Data':str(item.id), 'Message':returnMessage})
                return response
            else:
                response.content = json.dumps({'Success': False, 'Data': '0', 'Message': returnMessage})
                return response
        else:
            item = PermissionItemService.GetEntity(None, key)
            if item:
                item = item.loadJson(request)

            if curUser:
                item.modifiedby = curUser.RealName
                item.modifieduserid = curUser.Id
                item.modifiedon = datetime.datetime.now()
                returnCode, returnMessage = PermissionItemService.Update(None, item)
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
    entity = PermissionItemService.GetEntity(None, key)
    response = HttpResponse()
    response.content = entity.toJSON()
    return response

@LoginAuthorize
def Delete(request):
    try:
        key = request.POST['key']
    except:
        key = ''

    returnValue = PermissionItemService.SetDeleted(None, [key])

    if returnValue:
        response = HttpResponse()
        response.content = json.dumps({'Success': True, 'Data': '1', 'Message': FrameworkMessage.MSG0013})
        return response
    else:
        response = HttpResponse()
        response.content = json.dumps({'Success': False, 'Data': '0', 'Message': FrameworkMessage.MSG3020})
        return response

@LoginAuthorize
def MoveTo(request):
    try:
        key = request.POST['key']
    except:
        key = ''

    try:
        parentId = request.POST['parentId']
    except:
        parentId = ''

    if key and parentId:
        returnValue = PermissionItemService.MoveTo(None, key, parentId)
        if returnValue:
            response = HttpResponse()
            response.content = json.dumps({'Success': True, 'Data': '1', 'Message': '移动成功！'})
            return response
        else:
            response = HttpResponse()
            response.content = json.dumps({'Success': False, 'Data': '0', 'Message': '移动失败！'})
            return response
    else:
        response = HttpResponse()
        response.content = json.dumps({'Success': False, 'Data': '0', 'Message': '移动失败！'})
        return response