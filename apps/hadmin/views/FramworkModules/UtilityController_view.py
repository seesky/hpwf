# _*_ coding: utf-8 _*_
__author__ = 'baxuelong@163.com'
__date__ = '2019/1/18 13:20'

from apps.bizlogic.service.base.ItemDetailsService import ItemDetailsService
from django.http.response import HttpResponse
from apps.hadmin.MvcAppUtilties.LoginAuthorize import LoginAuthorize
from apps.utilities.publiclibrary.DbCommonLibaray import DbCommonLibaray
import xlwt
from io import BytesIO
import datetime
from django.template import loader ,Context

@LoginAuthorize
def GetCategory(request):
    try:
        code = request.GET['categoryCode']
    except:
        code = ''

    dtItemDetail = ItemDetailsService.GetDTByCode(None, code)

    returnValue = '['
    for item in dtItemDetail:
        returnValue = returnValue + item.toJSON() + ","
    returnValue = returnValue.strip(",")
    returnValue = returnValue + "]"

    response = HttpResponse()
    response.content = returnValue
    return response

@LoginAuthorize
def ExportExcel(request):
    fields = request.GET['fields']
    filters = request.GET['filters']
    tableName = request.GET['tableName']
    sortField = request.GET['sortField']

    if not sortField:
        sortField = "SORTCODE"

    dt = DbCommonLibaray.GetDTByPage(tableName, filters, sortField, fields, 1, 99999)

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename=' + tableName + str(datetime.datetime.now()) + '.xls'
    wb = xlwt.Workbook(encoding='utf8')
    sheet = wb.add_sheet(tableName)

    if len(dt) > 0:
        i = 0
        headerDic = []
        for headerKey in dt[0].keys():
            sheet.write(0, i, headerKey)
            headerDic.append(headerKey)
            i = i + 1

        data_row = 1
        for excelValue in dt:
            data_col = 0
            for header in headerDic:
                sheet.write(data_row, data_col, excelValue.get(header))
                data_col = data_col + 1
            data_row = data_row + 1

    output = BytesIO()
    wb.save(output)
    output.seek(0)
    response.write(output.getvalue())
    return response

@LoginAuthorize
def Search(request):
    response = HttpResponse()
    tmp = loader.get_template('Utility/Search.html')  # 加载模板
    render_content = {}  # 将要渲染到模板的数据
    new_body = tmp.render(render_content)  # 渲染模板
    response.content = new_body  # 设置返回内容
    return response
