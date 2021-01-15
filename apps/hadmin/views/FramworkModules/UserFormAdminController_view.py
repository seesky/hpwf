#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'baxuelong@163.com'
__date__ = '2021/1/13 16:08'

from django.http.response import HttpResponse
from apps.hadmin.MvcAppUtilties.LoginAuthorize import LoginAuthorize
from django.template import loader ,Context
from apps.hadmin.MvcAppUtilties.CommonUtils import CommonUtils
from django.views.decorators.csrf import csrf_exempt
from apps.hadmin.MvcAppUtilties.AjaxOnly import AjaxOnly
from apps.bizlogic.service.workflow.WorkFlowUserControl import WorkFlowUserControl
from apps.utilities.publiclibrary.SearchFilter import SearchFilter
import json
from apps.hadmin.MvcAppUtilties.JsonHelper import DateEncoder
from apps.bizlogic.models import MainUserControl
import uuid,datetime
from apps.utilities.message.StatusCode import StatusCode
from apps.utilities.message.FrameworkMessage import FrameworkMessage
from apps.bizlogic.models import MainUserControl as MainUserControlModule
from apps.bizlogic.models import UserControls

@csrf_exempt
@LoginAuthorize
def Index(request):
    """
    起始页
    Args:
    Returns:
    """
    response = HttpResponse()
    tmp = loader.get_template('UserFormAdmin/Index.html')  # 加载模板
    render_content = {'Skin': CommonUtils.Theme(response, request)}  # 将要渲染到模板的数据
    new_body = tmp.render(render_content)  # 渲染模板
    response.content = new_body  # 设置返回内容
    return response


@csrf_exempt
@LoginAuthorize
def MainUserControl(request):
    """
    起始页
    Args:
    Returns:
    """
    response = HttpResponse()
    tmp = loader.get_template('UserFormAdmin/MainUserControl.html')  # 加载模板
    render_content = {'Skin': CommonUtils.Theme(response, request)}  # 将要渲染到模板的数据
    new_body = tmp.render(render_content)  # 渲染模板
    response.content = new_body  # 设置返回内容
    return response

@csrf_exempt
@LoginAuthorize
def UserControlForm(request):
    """
    起始页
    Args:
    Returns:
    """
    response = HttpResponse()
    tmp = loader.get_template('UserFormAdmin/UserControlForm.html')  # 加载模板
    render_content = {'Skin': CommonUtils.Theme(response, request)}  # 将要渲染到模板的数据
    new_body = tmp.render(render_content)  # 渲染模板
    response.content = new_body  # 设置返回内容
    return response

@csrf_exempt
@LoginAuthorize
def MainUserControlLink(request):
    """
    起始页
    Args:
    Returns:
    """
    response = HttpResponse()
    tmp = loader.get_template('UserFormAdmin/MainUserControlLink.html.html')  # 加载模板
    render_content = {'Skin': CommonUtils.Theme(response, request)}  # 将要渲染到模板的数据
    new_body = tmp.render(render_content)  # 渲染模板
    response.content = new_body  # 设置返回内容
    return response


@csrf_exempt
@LoginAuthorize
def GetUserControlClass(request):
    response = HttpResponse()
    returnValue = '[{"id":"0","text":"表单管理","iconCls":"icon16_table_multiple","state":"open","children":[{"id":"1","text":"主表单管理","iconCls":"icon16_page_white_text","state":"open"},{"id":"2","text":"子表单管理","iconCls":"icon16_page_white_text","state":"open"}]}]'
    response.content = returnValue
    return response

@AjaxOnly
@LoginAuthorize
def GetMainUserControlByPage(request):
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



    dt = WorkFlowUserControl.GetMainUserControlByPage(CommonUtils.Current(response, request), SearchFilter.TransfromFilterToSql(filter, False), rows, sort + ' ' + order)

    recordCount = dt.count
    pageValue = dt.page(page)

    controlTmp = ''
    for control in pageValue:
        controlTmp = controlTmp + ', ' + json.dumps(control, cls=DateEncoder)
        controlTmp = controlTmp.strip(',')
    returnValue = '{"total": ' + str(recordCount) + ', "rows":[' + controlTmp + ']}'

    response.content = returnValue
    return response


@AjaxOnly
@LoginAuthorize
def GetUserControlByPage(request):
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

    dt = WorkFlowUserControl.GetUserInfoByPage(CommonUtils.Current(response, request),
                                                      SearchFilter.TransfromFilterToSql(filter, False), rows,
                                                      sort + ' ' + order)

    recordCount = dt.count
    pageValue = dt.page(page)

    controlTmp = ''
    for control in pageValue:
        controlTmp = controlTmp + ', ' + json.dumps(control, cls=DateEncoder)
        controlTmp = controlTmp.strip(',')
    returnValue = '{"total": ' + str(recordCount) + ', "rows":[' + controlTmp + ']}'

    response.content = returnValue
    return response


@AjaxOnly
@LoginAuthorize
def AddMainForm(request):
    try:
        IsOk = '1'
        try:
            fullname = request.POST['FullName']
        except:
            response = HttpResponse()
            response.content = json.dumps({'Success': False, 'Data': '0', 'Message': FrameworkMessage.MSG3020})
            return response

        try:
            en = request.POST['Enabled']
            if en == 'on':
                enabled = 1
        except:
            enabled = 0

        try:
            description = request.POST['Description']
        except:
            description = ''

        response = HttpResponse()

        curUser = CommonUtils.Current(response, request)


        entity = MainUserControlModule()


        entity.id = uuid.uuid4()
        # user.isstaff = 0
        # user.isvisible = 1
        # user.isdimission = 0
        entity.deletemark = 0
        entity.createon = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        entity.createby = curUser.RealName
        entity.createuserid = curUser.Id
        entity.modifiedon = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        entity.modifiedby = curUser.RealName
        entity.enabled = enabled
        entity.description = description
        entity.fullname = fullname

        returnCode, returnMessage, returnValue = WorkFlowUserControl.InsertMainUserCtrl(curUser, entity)


        if returnCode == StatusCode.statusCodeDic['OKAdd']:
            response.content = json.dumps({'Success':True, 'Data':IsOk, 'Message':returnMessage})
            return response
        else:
            response.content = json.dumps({'Success': False, 'Data': '0', 'Message': returnMessage})
            return response

    except Exception as e:
        print(e)
        response = HttpResponse()
        response.content = json.dumps({'Success': False, 'Data': '0', 'Message': FrameworkMessage.MSG3020})
        return response


@AjaxOnly
@LoginAuthorize
def EditMainForm(request):
    try:
        IsOk = '1'

        try:
            KeyId = request.POST['keyId']
        except:
            response = HttpResponse()
            response.content = json.dumps({'Success': False, 'Data': '0', 'Message': FrameworkMessage.MSG3020})
            return response

        try:
            fullname = request.POST['FullName']
        except:
            response = HttpResponse()
            response.content = json.dumps({'Success': False, 'Data': '0', 'Message': FrameworkMessage.MSG3020})
            return response

        try:
            en = request.POST['Enabled']
            if en == 'on':
                enabled = 1
        except:
            enabled = 0

        try:
            description = request.POST['Description']
        except:
            description = ''

        response = HttpResponse()

        curUser = CommonUtils.Current(response, request)

        entity = WorkFlowUserControl.GetMainUserCtrlEntity(None, KeyId)

        entity.fullname = fullname
        entity.enabled = enabled
        entity.description = description

        if curUser:
            entity.modifiedby = curUser.RealName
            entity.modifieduserid = curUser.Id
            entity.modifiedon = datetime.datetime.now()
            returnCode, returnMessage = WorkFlowUserControl.Update(None, entity)
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



@AjaxOnly
@LoginAuthorize
def DelMainForm(request):
    try:
        key = request.POST['keyId']
    except:
        key = ''

    returnValue = WorkFlowUserControl.SetDeleted(None, [key])

    if returnValue:
        response = HttpResponse()
        response.content = json.dumps({'Success': True, 'Data': '1', 'Message': FrameworkMessage.MSG0013})
        return response
    else:
        response = HttpResponse()
        response.content = json.dumps({'Success': False, 'Data': '0', 'Message': FrameworkMessage.MSG3020})
        return response



@AjaxOnly
@LoginAuthorize
def GetMainUserControlEntity(request):
    try:
        key = request.POST['keyId']
    except:
        key = None
    entity = WorkFlowUserControl.GetMainUserCtrlEntity(None, key)
    response = HttpResponse()
    response.content = entity.toJSON()
    return response



@AjaxOnly
@LoginAuthorize
def AddChildForm(request):
    try:
        IsOk = '1'
        try:
            fullname = request.POST['FullName']
        except:
            response = HttpResponse()
            response.content = json.dumps({'Success': False, 'Data': '0', 'Message': FrameworkMessage.MSG3020})
            return response



        try:
            en = request.POST['Enabled']
            if en == 'on':
                enabled = 1
        except:
            enabled = 0

        try:
            description = request.POST['Description']
        except:
            description = ''

        try:
            type = request.POST['Type']
        except:
            type = ''

        try:
            path = request.POST['Path']
        except:
            path = ''

        try:
            controlid = request.POST['ControlId']
        except:
            controlid = ''

        try:
            formname = request.POST['FormName']
        except:
            formname = ''

        try:
            assemblyname = request.POST['AssemblyName']
        except:
            assemblyname = ''




        response = HttpResponse()

        curUser = CommonUtils.Current(response, request)


        entity = UserControls()


        entity.id = uuid.uuid4()
        # user.isstaff = 0
        # user.isvisible = 1
        # user.isdimission = 0
        entity.deletemark = 0
        entity.createon = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        entity.createby = curUser.RealName
        entity.createuserid = curUser.Id
        entity.modifiedon = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        entity.modifiedby = curUser.RealName
        entity.enabled = enabled
        entity.description = description
        entity.fullname = fullname
        entity.path = path
        entity.controlid = controlid
        entity.formname = formname
        entity.assemblyname = assemblyname
        entity.type = type


        returnCode, returnMessage, returnValue = WorkFlowUserControl.InsertUserCtrl(curUser, entity)


        if returnCode == StatusCode.statusCodeDic['OKAdd']:
            response.content = json.dumps({'Success':True, 'Data':IsOk, 'Message':returnMessage})
            return response
        else:
            response.content = json.dumps({'Success': False, 'Data': '0', 'Message': returnMessage})
            return response

    except Exception as e:
        print(e)
        response = HttpResponse()
        response.content = json.dumps({'Success': False, 'Data': '0', 'Message': FrameworkMessage.MSG3020})
        return response


@AjaxOnly
@LoginAuthorize
def EditChildForm(request):
    try:
        IsOk = '1'

        try:
            KeyId = request.POST['keyId']
        except:
            response = HttpResponse()
            response.content = json.dumps({'Success': False, 'Data': '0', 'Message': FrameworkMessage.MSG3020})
            return response

        try:
            fullname = request.POST['FullName']
        except:
            response = HttpResponse()
            response.content = json.dumps({'Success': False, 'Data': '0', 'Message': FrameworkMessage.MSG3020})
            return response

        try:
            en = request.POST['Enabled']
            if en == 'on':
                enabled = 1
        except:
            enabled = 0

        try:
            description = request.POST['Description']
        except:
            description = ''

        try:
            path = request.POST['Path']
        except:
            path = ''

        try:
            type = request.POST['Type']
        except:
            type = ''

        try:
            controlid = request.POST['ControlId']
        except:
            controlid = ''

        try:
            formname = request.POST['FormName']
        except:
            formname = ''

        try:
            assemblyname = request.POST['AssemblyName']
        except:
            assemblyname = ''

        response = HttpResponse()

        curUser = CommonUtils.Current(response, request)

        entity = WorkFlowUserControl.GetUserCtrlEntity(None, KeyId)

        entity.fullname = fullname
        entity.enabled = enabled
        entity.description = description
        entity.fullname = fullname
        entity.path = path
        entity.controlid = controlid
        entity.formname = formname
        entity.assemblyname = assemblyname
        entity.type = type

        if curUser:
            entity.modifiedby = curUser.RealName
            entity.modifieduserid = curUser.Id
            entity.modifiedon = datetime.datetime.now()
            returnCode, returnMessage = WorkFlowUserControl.UpdateUserControl(None, entity)
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



@AjaxOnly
@LoginAuthorize
def DelChildForm(request):
    try:
        key = request.POST['keyId']
    except:
        key = ''

    returnValue = WorkFlowUserControl.DeleteUserControl(None, [key])

    if returnValue:
        response = HttpResponse()
        response.content = json.dumps({'Success': True, 'Data': '1', 'Message': FrameworkMessage.MSG0013})
        return response
    else:
        response = HttpResponse()
        response.content = json.dumps({'Success': False, 'Data': '0', 'Message': FrameworkMessage.MSG3020})
        return response


@AjaxOnly
@LoginAuthorize
def GetChildUserControlEntity(request):
    try:
        key = request.POST['keyId']
    except:
        key = None
    entity = WorkFlowUserControl.GetUserCtrlEntity(None, key)
    response = HttpResponse()
    response.content = entity.toJSON()
    return response