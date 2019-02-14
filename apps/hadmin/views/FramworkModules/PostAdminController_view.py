# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2019/1/11 14:07'

from django.template import loader ,Context
from apps.hadmin.MvcAppUtilties.PublicController import PublicController
from apps.hadmin.MvcAppUtilties.LoginAuthorize import LoginAuthorize
from django.http.response import HttpResponse
from apps.hadmin.MvcAppUtilties.CommonUtils import CommonUtils
from apps.bizlogic.service.base.RoleService import RoleService
from apps.bizlogic.models import Pirole
from apps.utilities.message.StatusCode import StatusCode
from apps.utilities.message.FrameworkMessage import FrameworkMessage
import json
import datetime
import uuid

def BuildToolBarButton(response, request):
    sb = ''
    linkbtnTemplate = "<a id=\"post_{0}\" class=\"easyui-linkbutton\" style=\"float:left\"  plain=\"true\" href=\"javascript:;\" icon=\"{1}\"  {2} title=\"{3}\">{4}</a>"
    sb = sb + "<a id=\"refresh\" class=\"easyui-linkbutton\" style=\"float:left\"  plain=\"true\" href=\"javascript:;\" icon=\"icon16_arrow_refresh\"  title=\"重新加载\">刷新</a> "
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

@LoginAuthorize
def Form(request):
    response = HttpResponse()
    tmp = loader.get_template('PostAdmin/Form.html')  # 加载模板
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

        try:
            OrganizeId = request.GET['OrganizeId']
        except:
            OrganizeId = None

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
            role.category = 'Duty'
            role.organizeid = OrganizeId
            role.createon = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            role.createby = curUser.RealName
            role.modifiedon = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            role.modifiedby = curUser.RealName
            role.createuserid = curUser.Id
            role.enabled = 1

            returnCode, returnMessage, returnValue = RoleService.Add(curUser, role)


            if returnCode == StatusCode.statusCodeDic['OKAdd']:
                response.content = json.dumps({'Success':True, 'Data':IsOk, 'Message':returnMessage})
                return response
            else:
                response.content = json.dumps({'Success': False, 'Data': '0', 'Message': returnMessage})
                return response
        else:
            role = RoleService.GetEntity(curUser, key)
            if role:
                role = role.loadJson(request)
            if curUser:
                role.modifiedby = curUser.RealName
                role.modifieduserid = curUser.Id
                returnCode, returnMessage = RoleService.Update(curUser, role)
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
    entity = RoleService.GetEntity(CommonUtils.Current(HttpResponse(), request), key)
    response = HttpResponse()
    response.content = entity.toJSON()
    return response

@LoginAuthorize
def Delete(request):
    try:
        key = request.POST['key']
    except:
        key = ''

    returnValue = RoleService.SetDeleted(CommonUtils.Current(HttpResponse(), request), [key])

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
        organizeId = request.POST['organizeId']
    except:
        organizeId = ''

    if key and organizeId:
        returnValue = RoleService.MoveTo(None, key, organizeId)
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