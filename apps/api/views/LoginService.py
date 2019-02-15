# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2019/2/15 13:37'

#import logging
#logging.basicConfig(level=logging.DEBUG)
from spyne import Application, rpc, ServiceBase,Integer, Unicode
from spyne import Iterable
from spyne.protocol.json import JsonDocument
from spyne.server.django import DjangoApplication
from django.views.decorators.csrf import csrf_exempt

from apps.utilities.publiclibrary.SystemInfo import SystemInfo
from apps.utilities.publiclibrary.UserInfo import UserInfo
import json
from apps.bizlogic.service.base.LogOnService import LogOnService
from apps.utilities.message.StatusCode import StatusCode
from apps.utilities.publiclibrary.SecretHelper import SecretHelper

class LoginService(ServiceBase):
    @rpc(Unicode, Unicode, _returns=Iterable(Unicode))
    def CheckLogin(ctx, Account, Password):
        if Account == SystemInfo.CurrentUserName:
            if Password == SystemInfo.CurrentPassword:
                imanageuser = UserInfo()
                imanageuser.Id = 'Administrator'
                imanageuser.UserName = '超级管理员'
                imanageuser.Code = 'Administrator'
                imanageuser.CompanyId = '系统'
                imanageuser.DepartmentId = '系统'
                imanageuser.IPAddress = ctx.transport.req["REMOTE_ADDR"]
                imanageuser.IsAdministrator = True
                # TODO:需要做在线人数统计


                user = json.dumps(imanageuser, default=UserInfo.obj_2_json)
                user = SecretHelper.AESEncrypt(user)
                Msg = str(user, encoding = "utf8")
            else:
                Msg = "['认证失败']"
        else:

            returnStatusCode = ''

            returnStatusCode, userInfo = LogOnService.UserLogOn(Account, Password, '', False, ctx.transport.req["REMOTE_ADDR"])

            if returnStatusCode == StatusCode.statusCodeDic.get('OK'):
                user = json.dumps(userInfo, default=UserInfo.obj_2_json)
                user = SecretHelper.AESEncrypt(user)
                Msg = str(user, encoding="utf8")
            else:
                Msg = "['认证失败']"

        yield Msg


login_application = Application([LoginService],
                          tns='Usable-Programming.LoginService.CheckLogin',
                          in_protocol = JsonDocument(validator='soft'),
                          out_protocol=JsonDocument())

login_service = csrf_exempt(DjangoApplication(login_application))