# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2019/2/15 16:13'

import logging
logging.basicConfig(level=logging.DEBUG)
from spyne import Application, rpc, ServiceBase,Integer, Unicode
from spyne import Iterable
from spyne.protocol.json import JsonDocument
from spyne.protocol.yaml import YamlDocument
from spyne.server.django import DjangoApplication
from django.views.decorators.csrf import csrf_exempt

from apps.utilities.publiclibrary.SystemInfo import SystemInfo
from apps.utilities.publiclibrary.UserInfo import UserInfo
import json
from apps.bizlogic.service.base.LogOnService import LogOnService
from apps.utilities.message.StatusCode import StatusCode
from apps.utilities.publiclibrary.SecretHelper import SecretHelper

from apps.bizlogic.service.base.UserOrganizeSerivce import UserOrganizeService
from apps.hadmin.MvcAppUtilties.JsonHelper import DateEncoder
from apps.hadmin.MvcAppUtilties.PublicController import PublicController
from apps.bizlogic.service.base.UserService import UserSerivce
from apps.utilities.publiclibrary.SearchFilter import SearchFilter

class UserAdminService(ServiceBase):
    @rpc(Unicode, Unicode, Unicode, Integer, Integer, _returns=Iterable(Unicode))
    def GetUserPageDTByDepartmentId(ctx, userInfo, organizeId, searchValue, page, rows):
        try:
            user = SecretHelper.AESDecrypt(userInfo)
            user = json.loads(user, object_hook=UserInfo.json_2_obj)
        except:
            yield "['认证失败']"


        if PublicController.ApiIsAuthorized(user, "UserManagement.GetUserPageDTByDepartmentId"):

            searchValue = searchValue if searchValue else ''

            jsons = "[]"
            returnValue = ''

            if organizeId:
                recordCount = 0
                recordCount, dtUser = UserOrganizeService.GetUserPageDTByDepartment(None, user, 'Resource.ManagePermission', searchValue, None, '', None, True, True, page, rows, 'sortcode', organizeId)
                userTmp = ''
                for user in dtUser:
                    userTmp = userTmp + ', ' + json.dumps(user, cls=DateEncoder)
                userTmp = userTmp.strip(',')
                returnValue = '{"total": ' + str(recordCount) + ', "rows":[' + userTmp + ']}'

                yield returnValue
            else:
                yield jsons
        else:
            yield "['权限不足']"

    @rpc(Unicode, Integer, Integer, Unicode, Unicode, Unicode, _returns=Iterable(Unicode))
    def GetUserListByPage(ctx, userInfo, page = 1, rows = 50, sort = 'sortcode', order = 'asc', filter = ''):

        try:
            user = SecretHelper.AESDecrypt(userInfo)
            user = json.loads(user, object_hook=UserInfo.json_2_obj)
        except:
            yield "['认证失败']"

        if PublicController.ApiIsAuthorized(user, "UserManagement.GetUserListByPage"):

            dtUser = UserSerivce.GetDTByPage(user,
                                             SearchFilter.TransfromFilterToSql(filter, False), '', '', rows,
                                             sort + ' ' + order)
            recordCount = dtUser.count
            pageValue = dtUser.page(page)

            userTmp = ''
            for role in pageValue:
                userTmp = userTmp + ', ' + json.dumps(role, cls=DateEncoder)
                userTmp = userTmp.strip(',')
            returnValue = '{"total": ' + str(recordCount) + ', "rows":[' + userTmp + ']}'
            yield returnValue
        else:
            yield "['权限不足']"





useradmin_application = Application([UserAdminService],
                          tns='Usable-Programming.UserAdminService.GetUserPageDTByDepartmentId',
                          in_protocol = JsonDocument(validator='soft'),
                          out_protocol=JsonDocument())

useradmin_service = csrf_exempt(DjangoApplication(useradmin_application))