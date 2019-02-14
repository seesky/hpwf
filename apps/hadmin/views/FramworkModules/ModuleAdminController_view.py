# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2019/1/11 16:06'

from django.template import loader ,Context
from apps.hadmin.MvcAppUtilties.PublicController import PublicController
from apps.hadmin.MvcAppUtilties.LoginAuthorize import LoginAuthorize
from django.http.response import HttpResponse
from apps.hadmin.MvcAppUtilties.CommonUtils import CommonUtils
from apps.utilities.publiclibrary.SystemInfo import SystemInfo
from apps.bizlogic.service.base.ModuleService import ModuleService
from apps.bizlogic.service.permission.ScopPermission import ScopPermission
from apps.utilities.message.StatusCode import StatusCode
from apps.utilities.message.FrameworkMessage import FrameworkMessage
from django.db.models import Q
from apps.bizlogic.models import Pimodule
import uuid
import datetime
import json

def BuildToolBarButton(response, request):
    sb = ''
    linkbtnTemplate = "<a id=\"a_{0}\" class=\"easyui-linkbutton\" style=\"float:left\"  plain=\"true\" href=\"javascript:;\" icon=\"{1}\"  {2} title=\"{3}\">{4}</a>"
    sb = sb + "<a id=\"a_refresh\" class=\"easyui-linkbutton\" style=\"float:left\"  plain=\"true\" href=\"javascript:;\" icon=\"icon16_arrow_refresh\"  title=\"重新加载\">刷新</a> "
    sb = sb + "<div class='datagrid-btn-separator'></div> "
    sb = sb + linkbtnTemplate.format("add", "icon16_tab_add", "" if PublicController.IsAuthorized(response, request, "ModuleManagement.Add") else "disabled=\"True\"", "新增模块（菜单）", "新增")
    sb = sb + linkbtnTemplate.format("edit", "icon16_tab_edit", "" if PublicController.IsAuthorized(response, request, "ModuleManagement.Edit") else "disabled=\"True\"", "修改选中的模块（菜单）", "修改")
    sb = sb + linkbtnTemplate.format("delete", "icon16_tab_delete", "" if PublicController.IsAuthorized(response, request, "ModuleManagement.Delete") else "disabled=\"True\"", "删除选中的模块（菜单）", "删除")
    #sb = sb + "<div class='datagrid-btn-separator'></div> "
    #sb = sb + linkbtnTemplate.format("export", "icon16_tab_go", "" if PublicController.IsAuthorized(response, request, "ModuleManagement.Export") else "disabled=\"True\"", "导出模块（菜单）数据", "导出")
    sb = sb + "<div class='datagrid-btn-separator'></div> "
    sb = sb + linkbtnTemplate.format("setusermodulepermission", "icon16_user_gladiator", "" if PublicController.IsAuthorized(response, request, "ModuleManagement.UserModulePermission") else "disabled=\"True\"", "设置用户的模块（菜单）访问权限", "用户模块权限")
    sb = sb + linkbtnTemplate.format("setrolemodulepermission", "icon16_group_key", "" if PublicController.IsAuthorized(response, request, "ModuleManagement.RoleModulePermission") else "disabled=\"True\"", "设置角色的模块（菜单）访问权限", "角色模块权限")
    sb = sb + "<div class='datagrid-btn-separator'></div> "
    #sb = sb + linkbtnTemplate.format("moduleconfig", "icon16_tab_content_vertical", "" if PublicController.IsAuthorized(response, request, "ModuleManagement.Edit") else "disabled=\"True\"", "设置模块的可用性", "模块配置")
    return sb

@LoginAuthorize
def Index(request):
    """
        起始页
        Args:
        Returns:
        """
    response = HttpResponse()
    tmp = loader.get_template('ModuleAdmin/Index.html')  # 加载模板
    render_content = {'Skin': CommonUtils.Theme(response, request),
                      'ToolButton': BuildToolBarButton(response, request)}  # 将要渲染到模板的数据
    new_body = tmp.render(render_content)  # 渲染模板
    response.content = new_body  # 设置返回内容
    return response

def GetModuleScope(response, request, permissionItemScopeCode):
    vUser = CommonUtils.Current(response, request)
    if vUser.IsAdministrator or (not permissionItemScopeCode) or (not SystemInfo.EnableUserAuthorizationScope):
        dtModule = ModuleService.GetDT(None)
        return dtModule
    else:
        dataTable = ScopPermission.GetModuleDTByPermissionScope(None, vUser.Id, permissionItemScopeCode)
        return dataTable

def GroupJsondata(groups, parentId):
    treeLevel = 0
    sb = ""
    list = []
    for g in groups:
        if g.parentid == parentId:
            list.append(g)
    for g in list:
        treeLevel = treeLevel + 1
        #jsons = json.dumps(g)
        #jsons = serializers.serialize('json', g)
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
def GetModuleTreeJson(request):
    isTree = None
    try:
        isTree = request.GET['isTree']
        if isTree == '1':
            isTree = True
        else:
            isTree = False
    except:
        isTree = True

    response = HttpResponse()

    dtModule = GetModuleScope(response, request, "Resource.ManagePermission")
    CommonUtils.CheckTreeParentId(dtModule, 'id', 'parentid')
    moduleJson = "[" + GroupJsondata(dtModule, "#") + "]"

    if isTree:
        response.content = moduleJson.replace("fullname", "text").replace("icon ", "").replace("\"iconcss\"", "\"iconCls\"").replace("expand", "state")
        return response
    else:
        response.content = moduleJson
        return response

def GetJsonData(dtModule):
    CommonUtils.CheckTreeParentId(dtModule, 'id', 'parentid')
    return "[" + GroupJsondata(dtModule, "#") + "]"

@LoginAuthorize
def GetModuleByIds(request):
    moduleIds = None
    try:
        moduleIds = request.POST['moduleIds']
    except:
        moduleIds = None
    dtPermissionItem = ModuleService.GetDTByIds(None, str(moduleIds).split(","))
    treeData = GetJsonData(dtPermissionItem)
    treeData = treeData.replace("icon ", "").replace("\"iconcss\"", "\"iconCls\"")
    response = HttpResponse()
    response.content = treeData
    return response

@LoginAuthorize
def Form(request):
    response = HttpResponse()
    tmp = loader.get_template('ModuleAdmin/Form.html')  # 加载模板
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
            module = Pimodule()
            module = module.loadJson(request)

            if not module.moduletype:
                module.moduletype = 6

            if not module.parentid:
                module.parentid = None

            if not module.navigateurl:
                module.navigateurl = '#'

            module.id = uuid.uuid4()
            # user.isstaff = 0
            # user.isvisible = 1
            # user.isdimission = 0
            module.deletemark = 0
            module.createon = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            module.createby = curUser.RealName
            module.createuserid = curUser.Id
            module.modifiedon = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            module.modifiedby = curUser.RealName
            module.enabled = 1

            returnCode, returnMessage, returnValue = ModuleService.Add(None, module)


            if returnCode == StatusCode.statusCodeDic['OKAdd']:
                response.content = json.dumps({'Success':True, 'Data':IsOk, 'Message':returnMessage})
                return response
            elif returnCode == StatusCode.statusCodeDic['ErrorCodeExist']:
                response.content = json.dumps({'Success': False, 'Data': '0', 'Message': '编码或名称重复'})
                return response
            else:
                response.content = json.dumps({'Success': False, 'Data': '0', 'Message': returnMessage})
                return response
        else:
            module = ModuleService.GetEntity(None, key)
            if module:
                module = module.loadJson(request)

            if curUser:
                module.modifiedby = curUser.RealName
                module.modifieduserid = curUser.Id
                module.modifiedon = datetime.datetime.now()
                returnCode, returnMessage = ModuleService.Update(None, module)
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
    entity = ModuleService.GetEntity(None, key)
    response = HttpResponse()
    response.content = entity.toJSON()
    return response


@LoginAuthorize
def Delete(request):
    try:
        key = request.POST['key']
    except:
        key = ''

    returnValue = ModuleService.SetDeleted(None, [key])

    if returnValue:
        response = HttpResponse()
        response.content = json.dumps({'Success': True, 'Data': '1', 'Message': FrameworkMessage.MSG0013})
        return response
    else:
        response = HttpResponse()
        response.content = json.dumps({'Success': False, 'Data': '0', 'Message': FrameworkMessage.MSG3020})
        return response