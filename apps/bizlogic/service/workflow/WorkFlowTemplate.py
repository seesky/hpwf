#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'baxuelong@163.com'
__date__ = '2021/1/7 15:19'

from apps.bizlogic.service.base.LogService import LogService
from apps.utilities.message.StatusCode import StatusCode
from apps.utilities.publiclibrary.DbCommonLibaray import DbCommonLibaray
from apps.utilities.message.FrameworkMessage import FrameworkMessage
import sys
from django.http.response import HttpResponse
from apps.hadmin.MvcAppUtilties.CommonUtils import CommonUtils

class WorkFlowTemplate(object):

    def GetAllowStartWorkFlows(self, userInfo, userId):
        """
        获取用户允许启动的工作流
        Args:
            userInfo (userInfo): 当前登录用户信息
            userId (string): 当前用户ID
        Returns:
            returnValue (List[]): 允许运行的工作流列表
        """
        LogService.WriteLog(userInfo, __class__.__name__, FrameworkMessage.UserService,
                            sys._getframe().f_code.co_name, FrameworkMessage.WorkFlowTemplateService_GetAllowsStartWorkFlows,
                            userId)

        sqlQuery = "SELECT  * FROM    ( SELECT  DISTINCT WFCLASSID ,CAPTION , FATHERID ,WORKFLOWID ,FLOWCAPTION ,WORKTASKID ,TASKCAPTION ,CLLEVEL ,MGRURL ,CLMGRURL FROM      WORKTASKVIEW WHERE     ( ( OPERCONTENT IN ( SELECT OPERCONTENT FROM   OPERCONTENTVIEW WHERE  USERID = '" + userId + "' ) ) OR ( OPERCONTENT IN ( SELECT  DEPARTMENTID FROM    V_PIUSER WHERE   ID = '" + userId + "' ) ) OR ( OPERCONTENT IN ( SELECT  ROLEID FROM    V_PIUSERROLE WHERE   USERID = '" + userId + "' ) ) OR ( OPERCONTENT = 'ALL' ) OR EXISTS ( SELECT * FROM   V_PIUSER WHERE  ID = '" + userId + "' AND ( CODE = 'Administrator' OR USERNAME = 'Administrator' ) )) AND TASKTYPEID = '1' AND STATUS = '1' UNION SELECT DISTINCT WFCLASSID ,CAPTION ,FATHERID ,WORKFLOWID ,FLOWCAPTION ,WORKTASKID ,TASKCAPTION ,CLLEVEL ,MGRURL ,CLMGRURL FROM      WORKTASKACCREDITVIEW WHERE     ACCREDITTOUSERID = '" + userId + "' AND ACCREDITSTATUS = '1' AND TASKTYPEID = '1' ) A   ORDER BY CLLEVEL ,CAPTION"

        returnValue = DbCommonLibaray.executeQuery(None, sqlQuery)

        return returnValue