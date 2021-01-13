#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'baxuelong@163.com'
__date__ = '2021/1/13 16:54'

from apps.bizlogic.service.base.LogService import LogService
from apps.utilities.message.StatusCode import StatusCode
from apps.utilities.message.FrameworkMessage import FrameworkMessage
import sys
from apps.utilities.publiclibrary.DbCommonLibaray import DbCommonLibaray
from django.core.paginator import Paginator

class WorkFlowUserControl(object):

    def GetMainUserControlByPage(userInfo, searchValue, rows=50, order=None):
        LogService.WriteLog(userInfo, __class__.__name__, FrameworkMessage.UserService,
                            sys._getframe().f_code.co_name, FrameworkMessage.WorkFlowUserControlService_GetMainUserControlByPage, '')

        myrecordCount = 0
        whereConditional = "DELETEMARK = 0 "

        if searchValue:
            whereConditional = whereConditional + "  AND (" + searchValue + ')'

        if order:
            whereConditional = whereConditional + " ORDER BY " + order

        sqlQuery = "SELECT  * FROM  MAINUSERCONTROL where " +  whereConditional

        dtList = DbCommonLibaray.executeQuery(None, sqlQuery)
        returnValue = Paginator(dtList, rows)
        return returnValue

    def GetUserInfoByPage(userInfo, searchValue, rows=50, order=None):
        LogService.WriteLog(userInfo, __class__.__name__, FrameworkMessage.UserService,
                            sys._getframe().f_code.co_name,
                            FrameworkMessage.WorkFlowUserControlService, '')

        myrecordCount = 0
        whereConditional = "DELETEMARK = 0 "

        if searchValue:
            whereConditional = whereConditional + "  AND (" + searchValue + ')'

        if order:
            whereConditional = whereConditional + " ORDER BY " + order

        sqlQuery = "SELECT  * FROM  USERCONTROLS where " + whereConditional

        dtList = DbCommonLibaray.executeQuery(None, sqlQuery)
        returnValue = Paginator(dtList, rows)
        return returnValue

