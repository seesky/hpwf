#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'baxuelong@163.com'
__date__ = '2021/1/5 8:56'

from django.http.response import HttpResponse
from apps.hadmin.MvcAppUtilties.LoginAuthorize import LoginAuthorize
from django.template import loader ,Context
from apps.hadmin.MvcAppUtilties.CommonUtils import CommonUtils
from django.views.decorators.csrf import csrf_exempt
from apps.bizlogic.service.workflow.WorkFlowTemplate import WorkFlowTemplate


@csrf_exempt
@LoginAuthorize
def Index(request):
    """
    起始页
    Args:
    Returns:
    """
    response = HttpResponse()
    tmp = loader.get_template('DailyBiz/Index.html')  # 加载模板
    render_content = {'Skin': CommonUtils.Theme(response, request)}  # 将要渲染到模板的数据
    new_body = tmp.render(render_content)  # 渲染模板
    response.content = new_body  # 设置返回内容
    return response


def FatherExist(dt, key):
    for dr in dt:
        if dr["WFCLASSID"] == key:
            return True
        else:
            continue
    return False

def LoadWorkflowClass(dt, key, returnValue):
    filter = "CLLEVEL='" + key + "'"
    dv = []
    for dr in dt:
        if dr["CLLEVEL"] == int(key):
            dv.append(dr)
        else:
            continue
    tmpClassId = "###"
    for row in dv:
        nowClassId = str(row["WFCLASSID"])
        if tmpClassId == nowClassId:
            continue
        tmpClassId = nowClassId
        returnValue = returnValue + "{{\"id\":\"{0}\",\"text\":\"{1}\",\"iconCls\":\"icon16_page_white_text\",\"attributes\":{{\"url\":\"{2}\"}},\"state\":\"open\"".format(tmpClassId, row["CAPTION"], row["CLMGRURL"])
        returnValue = LoadChildClass(dt, tmpClassId, returnValue)
        returnValue = returnValue + "},"

    return returnValue


def LoadChildClass(dt, key, returnValue):
    tmpClassId = "###"
    dv = []
    for dr in dt:
        if dr["FATHERID"] == key:
            dv.append(dr)
        else:
            continue
    if len(dv) > 0:
        returnValue = returnValue + ",\"children\":["

    for row in dv:
        nowClassId = str(row["WFCLASSID"])
        if tmpClassId == nowClassId:
            continue
        tmpClassId = nowClassId
        returnValue = returnValue + "{{\"id\":\"{0}\",\"text\":\"{1}\",\"iconCls\":\"icon16_page_white_text\",\"attributes\":{{\"url\":\"{2}\"}},\"state\":\"open\"".format(row["WFCLASSID"], row["CAPTION"], row["CLMGRURL"])
        LoadChildClass(dt, str(row["WFCLASSID"]), returnValue)
        returnValue = returnValue + "},"

    if (len(dv) > 0) and (len(returnValue) > 0):
        returnValue = returnValue[:-1]

    return returnValue

@csrf_exempt
@LoginAuthorize
def GetAvailableBizClass(request):
    response = HttpResponse()

    curUser = CommonUtils.Current(response, request)

    returnValue = '['
    returnValue += "{\"id\":\"#\",\"text\":\"日常业务\",\"iconCls\":\"icon16_table_multiple\",\"attributes\":{ \"url\": \"#\"},\"state\":\"open\""
    returnValue += ",\"children\":["

    dtAvailableBizClass = WorkFlowTemplate.GetAllowStartWorkFlows(None, curUser, curUser.Id)

    if (dtAvailableBizClass is not None) and (len(dtAvailableBizClass) > 0):
        cllevel = ''
        for dr in dtAvailableBizClass:
            nowcllevel = str(dr["CLLEVEL"])
            if nowcllevel == cllevel:
                continue
            clfathid = str(dr["FATHERID"])
            if FatherExist(dtAvailableBizClass, clfathid):
                continue
            returnValue = LoadWorkflowClass(dtAvailableBizClass, nowcllevel, returnValue)
            cllevel = nowcllevel
        returnValue = returnValue[:-1]

    returnValue = returnValue + "]}]"

    response.content = str(returnValue)
    return response

