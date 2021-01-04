# _*_ coding: utf-8 _*_
__author__ = 'baxuelong@163.com'
__date__ = '2018/12/11 15:41'

from apps.utilities.publiclibrary.SystemInfo import SystemInfo
from apps.bizlogic.models import Cilog
import time
from apps.utilities.publiclibrary.StringHelper import StringHelper
from apps.utilities.publiclibrary.DbCommonLibaray import DbCommonLibaray
from django.core.paginator import Paginator
from apps.bizlogic.service.base.PermissionScopeService import PermissionScopeService
import uuid,datetime

class LogService(object):

    def Add(userInfo, processName, methodName, processId, methodEngName, parameters):
        """
        添加日志信息
        Args:
            processName (string): 服务名称
            methodName (string): 方法名
            processId (string): 操作
            methodEngName (string): 操作名称
            parameters (string):  可记录的参数
        Returns:
            returnValue (string): 异常主键
        """
        if not SystemInfo.EnableRecordLog:
            return
        logEntity = Cilog()
        logEntity.id = uuid.uuid4()
        logEntity.ipaddress = userInfo.IPAddress
        logEntity.createon = datetime.datetime.now()
        logEntity.createuserid = userInfo.Id
        logEntity.userrealname = userInfo.RealName
        logEntity.processid = processId
        logEntity.processname = processName
        logEntity.methodengname = methodEngName
        logEntity.methodname = methodName
        logEntity.parameters = parameters
        logEntity.ipaddress = userInfo.IPAddress
        logEntity.createby = userInfo.RealName
        logEntity.createuserid = userInfo.Id
        logEntity.save()

    def WriteLog(userInfo, processId, processName, methodId, methodName, parameters):
        """
        写入日志
        Args:
            userInfo (UserInfo): 当前用户
            processId (string): 服务主键
            processName (string): 服务名称
            methodId (string): 操作
            methodName (string): 操作名称
        Returns:
        """
        if userInfo:
            LogService.Add(userInfo, processName, methodName, processId, methodId, parameters)
        else:
            return

    def WriteExit(userInfo, logId):
        """
        离开时的日志记录
        Args:
            userInfo (UserInfo): 用户
            logId (UserInfo): 日志主键
        Returns:
        """
        pass

    def GetLogGeneral(self):
        pass

    def GetDTByDate(userInfo, beginDate, endDate, userId, moduleId):
        """
        按时间获取列表
        Args:
            userInfo (UserInfo): 当前用户
            beginDate (string): 开始时间
            endDate (string): 结束时间
            userId (string): 用户主键
            moduleId (string): 模块主键
        Returns:
        """
        if userId:
            dataTable = DbCommonLibaray.executeQuery(None, LogService.GetDTSql([userId], 'processid', moduleId, beginDate, endDate))
        else:
            if userInfo.IsAdministrator:
                dataTable = DbCommonLibaray.executeQuery(None, LogService.GetDTSql(None, 'processid', moduleId, beginDate, endDate))
            else:
                userIds = PermissionScopeService.GetUserIds(None, userInfo.Id, "Resource.ManagePermission")
                dataTable = DbCommonLibaray.executeQuery(None, LogService.GetDTSql(userIds, 'processid', moduleId, beginDate, endDate))
        return dataTable

    def GetDTByModule(userInfo, processId, beginDate, endDate):
        """
        按模块获取日志
        Args:
            processId (string): 服务名称
            beginDate (datetime): 开始时间
            endDate (datetime): 结束时间
        Returns:
        """
        if userInfo.IsAdministrator:
            dataTable = DbCommonLibaray.executeQuery(None, LogService.GetDTSql(None, 'processid', processId, beginDate, endDate))
        else:
            userIds = PermissionScopeService.GetUserIds(None, userInfo.Id, "Resource.ManagePermission")
            dataTable = DbCommonLibaray.executeQuery(None, LogService.GetDTSql(userIds, 'processid', processId, beginDate, endDate))
        return dataTable

    def GetDTByUser(userId, beginDate, endDate):
        """
        按用户获取日志
        Args:
            userId (string): 用户主键
            beginDate (datetime): 开始时间
            endDate (datetime): 结束时间
        Returns:
        """
        returnValue = DbCommonLibaray.executeQuery(None, LogService.GetDTSql(None, 'userid', userId, beginDate, endDate))
        return returnValue


    def GetDTByPage(pageIndex=1, pageSize=20, whereConditional="", order=""):
        """
        获取系统操作日志分页列表
        Args:
            pageIndex (int): 当前页
            pageSize (int): 记录总数
            whereConditional (string): 条件表达式
            order (stirng): 排序字段
        Returns:
        """
        if whereConditional:
            whereConditional = "WHERE " + whereConditional
        if not order:
            order = " createon "
        sqlQuery = "select * from cilog " + whereConditional + " order by " + order

        dtLog = DbCommonLibaray.executeQuery(None, sqlQuery)
        pages = Paginator(dtLog, pageSize)
        recordCount = pages.count
        return recordCount, pages.page(pageIndex)

    def Delete(self, id):
        """
        删除日志
        Args:
            id (string): 主键
        Returns:
        """
        returnValue,v = Cilog.objects.filter(id=id).delete()
        return returnValue

    def BatchDelete(self, ids):
        """
        批量删除日志(业务)
        Args:
            ids (string[]): 主键数组
        Returns:
        """
        returnValue = Cilog.objects.filter(id__in=ids).delete()
        return returnValue

    def Truncate(self):
        """
       全部清除日志(业务)
       Args:
       Returns:
       """
        returnValue = Cilog.objects.all().delete()
        return returnValue

    def GetDTApplicationByDate(self, beginDate, endDate):
        """
        按日期获取日志（业务）
        Args:
            beginDate (datetime): 开始时间
            endDate (datetime): 结束时间
        Returns:
            returnValue (Cilog): 数据表
        """
        returnValue = DbCommonLibaray.executeQuery(None, LogService.GetDTSql(None, '', '', beginDate, endDate))
        return returnValue

    def BatchDeleteApplication(ids):
        """
        批量删除日志(业务)
        Args:
            ids (string[]): 主键数组
        Returns:
        """
        returnValue = Cilog.objects.filter(id__in=ids).delete()
        return returnValue

    def TruncateApplication(self):
        """
        全部清除日志(业务)
        Args:
        Returns:
        """
        returnValue = Cilog.objects.all().delete()
        return returnValue

    def GetDTSql(userIds, name, value, beginDate, endDate):
        sqlQuery = " SELECT * FROM " + 'cilog' + " WHERE 1=1 "

        if value:
            sqlQuery = sqlQuery +  " AND " + name + " = '" + value + "' "

        if beginDate and endDate:
            beginDate = str(time.strftime("%Y-%m-%d %H:%M:%S", beginDate))
            endDate = str(time.strftime("%Y-%m-%d %H:%M:%S", endDate))

        if userIds:
            sqlQuery = sqlQuery + " AND " + 'createuserid' + " IN (" + StringHelper.ObjectsToList(userIds) + ") "

        if len(beginDate.strip()) > 0:
            sqlQuery = sqlQuery + " AND CREATEON >= '" + beginDate + "'"
        if len(endDate.strip()) > 0:
            sqlQuery = sqlQuery + " AND CREATEON <= '" + endDate + "'"

        sqlQuery = sqlQuery + " ORDER BY CREATEON DESC "
        return sqlQuery
