# _*_ coding: utf-8 _*_
__author__ = 'baxuelong@163.com'
__date__ = '2019/1/16 14:08'

from apps.bizlogic.service.base.ExceptionService import ExceptionService
from apps.hadmin.MvcAppUtilties.CommonUtils import CommonUtils
from apps.hadmin.MvcAppUtilties.PublicController import PublicController
from apps.hadmin.MvcAppUtilties.LoginAuthorize import LoginAuthorize
from apps.hadmin.MvcAppUtilties.AjaxOnly import AjaxOnly
from apps.utilities.publiclibrary.SearchFilter import SearchFilter
from django.http.response import HttpResponse
from django.template import loader ,Context
import json
from apps.hadmin.MvcAppUtilties.JsonHelper import DateEncoder
from apps.bizlogic.service.base.ItemsService import ItemsService
from apps.bizlogic.service.base.ItemDetailsService import ItemDetailsService
from django.db.models import Q
from apps.bizlogic.service.base.ParameterService import ParameterService
from apps.bizlogic.models import Ciparameter
import uuid,datetime
from apps.utilities.message.StatusCode import StatusCode
from apps.utilities.message.FrameworkMessage import FrameworkMessage



def BuildToolBarButton(response, request):
    sb = ''
    linkbtnTemplate = "<a id=\"a_{0}\" class=\"easyui-linkbutton\" style=\"float:left\"  plain=\"true\" href=\"javascript:;\" icon=\"{1}\"  {2} title=\"{3}\">{4}</a>"
    sb = sb + "<a id=\"a_refresh\" class=\"easyui-linkbutton\" style=\"float:left\"  plain=\"true\" href=\"javascript:;\" icon=\"icon16_arrow_refresh\"  title=\"重新加载\">刷新</a> "
    sb = sb + "<div class='datagrid-btn-separator'></div> "
    sb = sb + linkbtnTemplate.format("add", "icon16_cog_add", "" if PublicController.IsAuthorized(response, request, "ParameterAdmin.Add") else "disabled=\"True\"", "新增序列", "新增")
    sb = sb + linkbtnTemplate.format("edit", "icon16_cog_edit", "" if PublicController.IsAuthorized(response, request, "ParameterAdmin.Edit") else "disabled=\"True\"", "修改选中序列", "修改")
    sb = sb + linkbtnTemplate.format("del", "icon16_cog_delete", "" if PublicController.IsAuthorized(response, request, "ParameterAdmin.Delete") else "disabled=\"True\"", "删除选中序列", "删除")
    sb = sb + "<div class='datagrid-btn-separator'></div> "
    sb = sb + linkbtnTemplate.format("export", "icon16_cog_go", "" if PublicController.IsAuthorized(response, request, "ParameterAdmin.Export") else "disabled=\"True\"", "导出序列数据", "导出")
    return sb


@LoginAuthorize
def Index(request):
    """
    起始页
    Args:
    Returns:
    """
    response = HttpResponse()
    tmp = loader.get_template('ParameterAdmin/Index.html')  # 加载模板
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

    recordCount, dtParameter = ParameterService.GetDTByPage(CommonUtils.Current(response, request), SearchFilter.TransfromFilterToSql(filter, False), rows,  sort + ' ' + order)
    pageValue = dtParameter.page(page)

    parameterTmp = ''
    for parameter in pageValue:
        parameterTmp = parameterTmp + ', ' + json.dumps(parameter, cls=DateEncoder)
    parameterTmp = parameterTmp.strip(',')
    returnValue = '{"total": ' + str(recordCount) + ', "rows":[' + parameterTmp + ']}'

    response.content = returnValue
    return response

@LoginAuthorize
def Form(request):
    response = HttpResponse()
    tmp = loader.get_template('ParameterAdmin/Form.html')  # 加载模板
    render_content = {}  # 将要渲染到模板的数据
    new_body = tmp.render(render_content)  # 渲染模板
    response.content = new_body  # 设置返回内容
    return response

@LoginAuthorize
def GetEntity(request):
    try:
        key = request.POST['key']
    except:
        key = None
    entity = ParameterService.GetEntity(CommonUtils.Current(HttpResponse(), request), key)
    response = HttpResponse()
    response.content = entity.toJSON()
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
            parameter = Ciparameter()
            parameter = parameter.loadJson(request)

            parameter.id = uuid.uuid4()
            parameter.deletemark = 0
            parameter.createon = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            parameter.createby = curUser.RealName
            parameter.createuserid = curUser.Id
            parameter.modifiedon = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            parameter.modifiedby = curUser.RealName
            parameter.enabled = 1

            returnCode, returnMessage, returnValue = ParameterService.Add(curUser, parameter)


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
            parameter = ParameterService.GetEntity(CommonUtils.Current(response, request), key)
            if parameter:
                parameter = parameter.loadJson(request)
            else:
                response.content = json.dumps({'Success': False, 'Data': '0', 'Message': "修改失败！"})
                return response

            if curUser:
                parameter.modifiedby = curUser.RealName
                parameter.modifieduserid = curUser.Id
                parameter.modifiedon = datetime.datetime.now()
                returnCode, returnMessage = ParameterService.Update(CommonUtils.Current(response, request), parameter)
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
def Delete(request):
    try:
        key = request.POST['key']
    except:
        key = ''

    returnValue = ParameterService.SetDeleted(CommonUtils.Current(HttpResponse(), request), key)

    if returnValue > 0:
        response = HttpResponse()
        response.content = json.dumps({'Success': True, 'Data': '1', 'Message': FrameworkMessage.MSG0013})
        return response
    else:
        response = HttpResponse()
        response.content = json.dumps({'Success': False, 'Data': '0', 'Message': FrameworkMessage.MSG3020})
        return response