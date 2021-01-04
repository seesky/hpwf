# _*_ coding: utf-8 _*_
__author__ = 'baxuelong@163.com'
__date__ = '2019/1/16 13:22'

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
from apps.bizlogic.models import Ciitems
from apps.bizlogic.models import Ciitemdetails
import uuid,datetime
from apps.utilities.message.StatusCode import StatusCode
from apps.utilities.message.FrameworkMessage import FrameworkMessage


def BuildToolBarButton(response, request):
    sb = ''
    linkbtnTemplate = "<a id=\"a_{0}\" class=\"easyui-linkbutton\" style=\"float:left\"  plain=\"true\" href=\"javascript:;\" icon=\"{1}\"  {2} title=\"{3}\">{4}</a>"
    sb = sb + "<a id=\"a_refresh\" class=\"easyui-linkbutton\" style=\"float:left\"  plain=\"true\" href=\"javascript:;\" icon=\"icon16_arrow_refresh\"  title=\"重新加载\">刷新</a> "
    sb = sb + "<div class='datagrid-btn-separator'></div> "
    sb = sb + linkbtnTemplate.format("itemdetailadd", "icon16_table_add", "" if PublicController.IsAuthorized(response, request, "DictionaryDetail.Add") else "disabled=\"True\"", "新增字典明细项", "新增")
    sb = sb + linkbtnTemplate.format("itemdetailedit", "icon16_table_edit", "" if PublicController.IsAuthorized(response, request, "DictionaryDetail.Edit") else "disabled=\"True\"", "修改选中的字典明细项", "修改")
    sb = sb + linkbtnTemplate.format("itemdetaildelete", "icon16_table_delete", "" if PublicController.IsAuthorized(response, request, "DictionaryDetail.Delete") else "disabled=\"True\"", "删除选中的字典明细项", "删除")
    return sb


@LoginAuthorize
def Index(request):
    """
    起始页
    Args:
    Returns:
    """
    response = HttpResponse()
    tmp = loader.get_template('DataItemAdmin/Index.html')  # 加载模板
    render_content = {'Skin': CommonUtils.Theme(response, request),
                      'ToolButton': BuildToolBarButton(response, request)}  # 将要渲染到模板的数据
    new_body = tmp.render(render_content)  # 渲染模板
    response.content = new_body  # 设置返回内容
    return response

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

def GetDataItemTreeJson(request):
    isTree = None
    try:
        isTree = request.GET['isTree']
        if isTree == '1':
            isTree = True
        else:
            isTree = False
    except:
        isTree = False

    jsons = '[]'
    response = HttpResponse()
    dtItems = ItemsService.GetDT(CommonUtils.Current(response, request))
    CommonUtils.CheckTreeParentId(dtItems, 'id', 'parentid')
    itemJson = "[" + GroupJsondata(dtItems, "#") + "]"
    if isTree:
        response.content = itemJson.replace("fullname", "text")
        return response
    else:
        response.content = itemJson
        return response

def GetDataItemDetailById(request):
    jsonStr = '[]'
    try:
        categoryId = request.POST['categoryId']
    except:
        categoryId = None
    if categoryId:
        dtItemDetail = ItemDetailsService.GetDTByValues({'deletemark':'0', 'itemid':categoryId})
        CommonUtils.CheckTreeParentId(dtItemDetail, 'id', 'itemid')

        if dtItemDetail and len(dtItemDetail) > 0:
            jsonStr = "[" + GroupJsondata(dtItemDetail, "#") + "]"
        response = HttpResponse()
        response.content = jsonStr
        return response
    else:
        response = HttpResponse()
        response.content = jsonStr
        return response

def DataItemDetail(request):
    response = HttpResponse()
    tmp = loader.get_template('DataItemAdmin/DataItemDetail.html')  # 加载模板
    render_content = {}  # 将要渲染到模板的数据
    new_body = tmp.render(render_content)  # 渲染模板
    response.content = new_body  # 设置返回内容
    return response

def DataItem(request):
    response = HttpResponse()
    tmp = loader.get_template('DataItemAdmin/DataItem.html')  # 加载模板
    render_content = {}  # 将要渲染到模板的数据
    new_body = tmp.render(render_content)  # 渲染模板
    response.content = new_body  # 设置返回内容
    return response

@LoginAuthorize
def SubmitItemsForm(request):
    try:
        IsOk = '1'
        try:
            key = request.GET['key']
        except:
            key = None

        response = HttpResponse()

        curUser = CommonUtils.Current(response, request)

        if not key:
            item = Ciitems()
            item = item.loadJson(request)

            item.id = uuid.uuid4()
            item.deletemark = 0
            item.createon = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            item.createby = curUser.RealName
            item.createuserid = curUser.Id
            item.modifiedon = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            item.modifiedby = curUser.RealName
            item.enabled = 1
            item.allowedit = 1
            item.allowdelete = 1

            returnValue, returnMessage = ItemsService.Add(curUser, item)


            if returnValue == 1:
                response.content = json.dumps({'Success':True, 'Data':'1', 'Message':returnMessage})
                return response
            elif returnValue == 0:
                response.content = json.dumps({'Success': False, 'Data': '0', 'Message': '编码或名称重复'})
                return response
            else:
                response.content = json.dumps({'Success': False, 'Data': '0', 'Message': returnMessage})
                return response
        else:
            item = ItemsService.GetEntity(CommonUtils.Current(response, request), key)
            if item:
                parameter = item.loadJson(request)
            else:
                response.content = json.dumps({'Success': False, 'Data': '0', 'Message': "修改失败！"})
                return response

            if curUser:
                response.modifiedby = curUser.RealName
                response.modifieduserid = curUser.Id
                response.modifiedon = datetime.datetime.now()
                returnCode, returnMessage = ItemsService.Update(CommonUtils.Current(response, request), parameter)
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
def SubmitItemsDetailForm(request):
    try:
        IsOk = '1'
        try:
            key = request.GET['key']
        except:
            key = None

        response = HttpResponse()

        curUser = CommonUtils.Current(response, request)

        if not key:
            item = Ciitemdetails()
            item = item.loadJson(request)

            item.id = uuid.uuid4()
            item.deletemark = 0
            item.createon = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            item.createby = curUser.RealName
            item.createuserid = curUser.Id
            item.modifiedon = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            item.modifiedby = curUser.RealName
            item.enabled = 1

            returnValue, returnMessage = ItemDetailsService.Add(curUser, item)


            if returnValue == 1:
                response.content = json.dumps({'Success':True, 'Data':'1', 'Message':returnMessage})
                return response
            elif returnValue == 0:
                response.content = json.dumps({'Success': False, 'Data': '0', 'Message': '编码或名称重复'})
                return response
            else:
                response.content = json.dumps({'Success': False, 'Data': '0', 'Message': returnMessage})
                return response
        else:
            item = ItemDetailsService.GetEntity(CommonUtils.Current(response, request), key)
            if item:
                parameter = item.loadJson(request)
            else:
                response.content = json.dumps({'Success': False, 'Data': '0', 'Message': "修改失败！"})
                return response

            if curUser:
                response.modifiedby = curUser.RealName
                response.modifieduserid = curUser.Id
                response.modifiedon = datetime.datetime.now()
                returnCode, returnMessage = ItemsService.Update(CommonUtils.Current(response, request), parameter)
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
def DeleteDataItem(request):
    try:
        key = request.POST['key']
    except:
        key = ''

    returnValue = ItemsService.SetDeleted(CommonUtils.Current(HttpResponse(), request), [key])

    if returnValue:
        response = HttpResponse()
        response.content = json.dumps({'Success': True, 'Data': '1', 'Message': FrameworkMessage.MSG0013})
        return response
    else:
        response = HttpResponse()
        response.content = json.dumps({'Success': False, 'Data': '0', 'Message': FrameworkMessage.MSG3020})
        return response

@LoginAuthorize
def DeleteItemDetail(request):
    try:
        key = request.POST['key']
    except:
        key = ''

    returnValue = ItemDetailsService.SetDeleted(CommonUtils.Current(HttpResponse(), request), [key])

    if returnValue:
        response = HttpResponse()
        response.content = json.dumps({'Success': True, 'Data': '1', 'Message': FrameworkMessage.MSG0013})
        return response
    else:
        response = HttpResponse()
        response.content = json.dumps({'Success': False, 'Data': '0', 'Message': FrameworkMessage.MSG3020})
        return response

@LoginAuthorize
def GetItemsEntity(request):
    try:
        key = request.POST['key']
    except:
        key = None
    entity = ItemsService.GetEntity(CommonUtils.Current(HttpResponse(), request), key)
    response = HttpResponse()
    response.content = entity.toJSON()
    return response

@LoginAuthorize
def GetItemsDetailEntity(request):
    try:
        key = request.POST['key']
    except:
        key = None
    entity = ItemDetailsService.GetEntity(CommonUtils.Current(HttpResponse(), request), key)
    response = HttpResponse()
    response.content = entity.toJSON()
    return response
