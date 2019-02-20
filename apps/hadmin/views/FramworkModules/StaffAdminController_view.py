# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2019/1/10 13:38'

from apps.hadmin.MvcAppUtilties.LoginAuthorize import LoginAuthorize
from apps.hadmin.MvcAppUtilties.IsAuthorized import IsAuthorized
from django.http.response import HttpResponse
from django.template import loader ,Context
from apps.hadmin.MvcAppUtilties.CommonUtils import CommonUtils
from apps.hadmin.MvcAppUtilties.PublicController import PublicController
from apps.utilities.message.StatusCode import StatusCode
from apps.utilities.message.FrameworkMessage import FrameworkMessage
from apps.hadmin.MvcAppUtilties.AjaxOnly import AjaxOnly
from apps.bizlogic.service.base.StaffService import StaffService
from apps.bizlogic.models import Pistaff
import json
import uuid
import datetime
from apps.bizlogic.service.base.SequenceService import SequenceService


def BuildToolBarButton(response, request):
    sb = ''
    linkbtnTemplate = "<a id=\"btn{0}\" class=\"easyui-linkbutton\" style=\"float:left\"  plain=\"true\" href=\"javascript:;\" icon=\"{1}\"  {2} title=\"{3}\">{4}</a>"
    sb = sb + "<a id=\"btnRefresh\" class=\"easyui-linkbutton\" style=\"float:left\"  plain=\"true\" href=\"javascript:;\" icon=\"icon16_arrow_refresh\"  title=\"重新加载\">刷新</a> "
    sb = sb + "<div class='datagrid-btn-separator'></div> "
    sb = sb + linkbtnTemplate.format("AddStaff", "icon16_vcard_add", "" if PublicController.IsAuthorized(response, request, "StaffAdmin.Add") else "disabled=\"True\"", "添加员工", "添加")
    sb = sb + linkbtnTemplate.format("EditStaff", "icon16_vcard_edit", "" if PublicController.IsAuthorized(response, request, "StaffAdmin.Edit") else "disabled=\"True\"", "修改员工", "修改")
    sb = sb + linkbtnTemplate.format("DeleteStaff", "icon16_vcard_delete", "" if PublicController.IsAuthorized(response, request, "StaffAdmin.Delete") else "disabled=\"True\"", "删除员工", "删除")
    sb = sb + "<div class='datagrid-btn-separator'></div> "
    sb = sb + linkbtnTemplate.format("MoveTo", "icon16_arrow_switch", "" if PublicController.IsAuthorized(response, request, "StaffAdmin.Move") else "disabled=\"True\"", "移动选中的员工", "移动")
    sb = sb + "<div class='datagrid-btn-separator'></div> "
    sb = sb + linkbtnTemplate.format("Export", "icon16_user_go", "" if PublicController.IsAuthorized(response, request, "StaffAdmin.Export") else "disabled=\"True\"", "导出员工数据", "导出")
    return sb

@LoginAuthorize
def Index(request):
    """
    起始页
    Args:
    Returns:
    """
    response = HttpResponse()
    tmp = loader.get_template('StaffAdmin/Index.html')  # 加载模板
    render_content = {'Skin': CommonUtils.Theme(response, request),
                      'ToolButton': BuildToolBarButton(response, request)}  # 将要渲染到模板的数据
    new_body = tmp.render(render_content)  # 渲染模板
    response.content = new_body  # 设置返回内容
    return response

@AjaxOnly
@LoginAuthorize
def GetStaffByOrganizeId(request):
    """
    起始页
    Args:
    Returns:
    """
    jsons = "[]"
    organizeId = None
    try:
        organizeId = request.POST['organizeId']
    except:
        organizeId = None

    response = HttpResponse()
    returnValue = '['

    if organizeId:
        recordCount = 0
        dtStaff = StaffService.GetDTByOrganize(CommonUtils.Current(response, request), organizeId, True)
        for staff in dtStaff:
            returnValue = returnValue + staff.toJSON() + ","
        returnValue = returnValue.strip(",")
        returnValue = returnValue + "]"
        response.content = returnValue
    else:
        response.content = jsons

    return response

@LoginAuthorize
def Form(request):
    """
    起始页
    Args:
    Returns:
    """
    response = HttpResponse()
    tmp = loader.get_template('StaffAdmin/Form.html')  # 加载模板
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
            organizeId = request.GET['organizeId']
        except:
            organizeId = ''

        response = HttpResponse()

        curUser = CommonUtils.Current(response, request)

        if not key:
            staff = Pistaff()
            staff = staff.loadJson(request)

            staff.id = uuid.uuid4()
            # user.isstaff = 0
            # user.isvisible = 1
            # user.isdimission = 0
            staff.deletemark = 0
            staff.createon = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            staff.createby = curUser.RealName
            staff.modifiedon = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            staff.modifiedby = curUser.RealName
            staff.enabled = 1
            staff.isdimission = 0

            if staff.sortcode == None or staff.sortcode == 0:
                sequence = SequenceService.GetSequence(None, 'PISTAFF')
                staff.sortcode = int(sequence)



            if not organizeId:
                returnCode, returnMessage, returnValue = StaffService.Add(CommonUtils.Current(response, request), staff)
            else:
                returnCode, returnMessage, returnValue = StaffService.Add(CommonUtils.Current(response, request), staff, organizeId)


            if returnCode == StatusCode.statusCodeDic['OKAdd']:
                response.content = json.dumps({'Success':True, 'Data':IsOk, 'Message':returnMessage})
                return response
            else:
                response.content = json.dumps({'Success': False, 'Data': '0', 'Message': returnMessage})
                return response
        else:
            staffEntity = StaffService.GetEntity(CommonUtils.Current(response, request), key)
            if staffEntity:
                staffEntity = staffEntity.loadJson(request)

            if curUser:
                staffEntity.modifiedby = curUser.RealName
                staffEntity.modifieduserid = curUser.Id
                returnCode, returnMessage = StaffService.UpdateStaff(CommonUtils.Current(response, request), staffEntity)
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
    entity = StaffService.GetEntity(CommonUtils.Current(HttpResponse(), request), key)
    response = HttpResponse()
    response.content = entity.toJSON()
    return response

@LoginAuthorize
def Delete(request):
    try:
        key = request.POST['key']
    except:
        key = ''

    returnValue = StaffService.SetDeleted(CommonUtils.Current(HttpResponse(), request), [key])

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
        staffId = request.POST['staffId']
    except:
        staffId = ''

    try:
        organizeId = request.POST['organizeId']
    except:
        organizeId = ''

    if staffId and organizeId:
        returnValue = StaffService.MoveTo(CommonUtils.Current(HttpResponse(), request), staffId, organizeId)
        if returnValue:
            response = HttpResponse()
            response.content = json.dumps({'Success': True, 'Data': '1', 'Message': FrameworkMessage.MSG0013})
            return response
        else:
            response = HttpResponse()
            response.content = json.dumps({'Success': False, 'Data': '0', 'Message': FrameworkMessage.MSG3020})
            return response

    else:
        response = HttpResponse()
        response.content = json.dumps({'Success': False, 'Data': '0', 'Message': FrameworkMessage.MSG3020})
        return response
