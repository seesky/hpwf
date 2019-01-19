# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2019/1/18 13:20'

from apps.bizlogic.service.base.ItemDetailsService import ItemDetailsService
from django.http.response import HttpResponse

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