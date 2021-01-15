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
from django.db.utils import DatabaseError
from django.db.transaction import TransactionManagementError
from apps.bizlogic.models import MainUserControl
from apps.bizlogic.models import UserControls

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

    def InsertMainUserCtrl(userInfo, entity):
        LogService.WriteLog(userInfo, __class__.__name__, FrameworkMessage.WorkFlowUserControlService,
                            sys._getframe().f_code.co_name,
                            FrameworkMessage.WorkFlowUserControlService_InsertMainUserCtrl, '')
        try:
            entity.save()
            returnCode = StatusCode.statusCodeDic['OKAdd']
            returnMessage = FrameworkMessage.MSG0009
            returnValue = entity.id
            return returnCode, returnMessage, returnValue
        except DatabaseError as e:
            print(e)
            returnCode = StatusCode.statusCodeDic['DbError']
            returnMessage = FrameworkMessage.MSG0001
            returnValue = None
            return returnCode, returnMessage, returnValue
        except TransactionManagementError as e:
            print(e)
            returnCode = StatusCode.statusCodeDic['DbError']
            returnMessage = FrameworkMessage.MSG0001
            returnValue = None
            return returnCode, returnMessage, returnValue

    def GetMainUserCtrlEntity(self, id):
        """
        按主键数组获取列表
        Args:
            id (string): 主键
        Returns:
            returnValue (MainUserControl or None): 模块实体
        """
        try:
            returnValue = MainUserControl.objects.get(id=id)
        except MainUserControl.DoesNotExist as e:
            returnValue = None
        return returnValue

    def Update(self, entity):
        try:
            entity.save()
            returnCode = StatusCode.statusCodeDic['OKUpdate']
            returnMessage = FrameworkMessage.MSG0010
            return returnCode, returnMessage
        except Exception as ex:
            returnCode = StatusCode.statusCodeDic['Error']
            returnMessage = ex
            return returnCode, returnMessage

    def SetDeleted(self, ids):
        """
        批量打删除标志
        Args:
            ids (string): 主键数组
        Returns:
            returnValue (True or False): 删除结果
        """
        try:
            organize = MainUserControl.objects.filter(id__in=ids).update(deletemark=1)
            return True
        except Exception as e:
            return False

    def InsertUserCtrl(userInfo, entity):
        LogService.WriteLog(userInfo, __class__.__name__, FrameworkMessage.WorkFlowUserControlService,
                            sys._getframe().f_code.co_name,
                            FrameworkMessage.WorkFlowUserControlService_InsertUserControl, '')
        try:
            entity.save()
            returnCode = StatusCode.statusCodeDic['OKAdd']
            returnMessage = FrameworkMessage.MSG0009
            returnValue = entity.id
            return returnCode, returnMessage, returnValue
        except DatabaseError as e:
            print(e)
            returnCode = StatusCode.statusCodeDic['DbError']
            returnMessage = FrameworkMessage.MSG0001
            returnValue = None
            return returnCode, returnMessage, returnValue
        except TransactionManagementError as e:
            print(e)
            returnCode = StatusCode.statusCodeDic['DbError']
            returnMessage = FrameworkMessage.MSG0001
            returnValue = None
            return returnCode, returnMessage, returnValue

    def GetUserCtrlEntity(self, id):
        """
        按主键数组获取列表
        Args:
            id (string): 主键
        Returns:
            returnValue (MainUserControl or None): 模块实体
        """
        try:
            returnValue = UserControls.objects.get(id=id)
        except MainUserControl.DoesNotExist as e:
            returnValue = None
        return returnValue

    def UpdateUserControl(self, entity):
        try:
            entity.save()
            returnCode = StatusCode.statusCodeDic['OKUpdate']
            returnMessage = FrameworkMessage.MSG0010
            return returnCode, returnMessage
        except Exception as ex:
            returnCode = StatusCode.statusCodeDic['Error']
            returnMessage = ex
            return returnCode, returnMessage

    def DeleteUserControl(self, ids):
        """
        批量打删除标志
        Args:
            ids (string): 主键数组
        Returns:
            returnValue (True or False): 删除结果
        """
        try:
            organize = UserControls.objects.filter(id__in=ids).update(deletemark=1)
            return True
        except Exception as e:
            return False