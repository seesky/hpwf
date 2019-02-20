# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2018/12/11 16:02'

from apps.bizlogic.models import Ciexception
from apps.utilities.publiclibrary.DbCommonLibaray import DbCommonLibaray
from django.core.paginator import Paginator
from django.db.utils import DatabaseError
from django.db.transaction import TransactionManagementError
from django.db.models import Q
from utilities.message.StatusCode import StatusCode
from utilities.message.FrameworkMessage import FrameworkMessage
from apps.bizlogic.service.base.LogService import LogService
import sys


class ExceptionService(object):
    def Add(self, entity):
        """
        添加异常数据
        Args:
            entity (Ciexception): 异常主键
        Returns:
            returnValue (string): 异常主键
        """
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

    def GetDT(self):
        """
        取得列表
        Args:
        Returns:
            returnValue (Ciexception[]): 异常实体列表
        """
        returnValue = Ciexception.objects.all()
        return returnValue

    def GetDTByPage(pageIndex=1, pageSize=20, whereConditional="", order=""):
        """
        获取系统异常分页列表
        Args:
            searchValue (string): 查询字段
            departmentId (string): 部门主键
            roleId (string): 角色主键
            pageSize (int): 每页显示
            order (string): 排序
        Returns:
            returnValue (Paginator): 异常分页列表
        """
        if whereConditional:
            whereConditional = "WHERE " + whereConditional
        if not order:
            order = " createon "
        sqlQuery = "select * from ciexception " + whereConditional + " order by " + order

        dtException = DbCommonLibaray.executeQuery(None, sqlQuery)
        pages = Paginator(dtException, pageSize)
        recordCount = pages.count
        return recordCount, pages.page(pageIndex)

    def GetEntity(self, id):
        """
        获取实体
        Args:
            id (string): 主键
        Returns:
            returnValue (Ciexception): 异常实体
        """
        returnValue = Ciexception.objects.filter(id=id)
        return returnValue

    def GetDTByValues(self, valueDic):
        """
        按键值对获取列表
        valueDic = {key:value, key:value, ...}
        Args:
            valueDic (Dic{key:value}): 参数和值对
        Returns:
            returnValue (Pioranize[]): 组织机构列表
        """
        q = Q()
        for i in valueDic:
            q.add(Q(**{i: valueDic[i]}), Q.AND)
        returnValue = Ciexception.objects.filter(q)
        return returnValue

    def Delete(userInfo, ids):
        """
        删除异常
        Args:
            id (string): 主键
        Returns:
            returnValue (int): 受影响行数
        """
        LogService.WriteLog(userInfo, __class__.__name__, FrameworkMessage.ExceptionService,
                            sys._getframe().f_code.co_name, FrameworkMessage.ExceptionService_Delete, '')
        returnValue,v = Ciexception.objects.filter(id__in=ids).delete()
        # returnValue = 0
        # for id in ids:
        #     returnValue = returnValue + Ciexception.objects.filter(id=id).delete()

        return returnValue

    def BatchDelete(self, ids):
        """
        批量删除异常
        Args:
            ids (string): 主键列表
        Returns:
            returnValue (int): 受影响行数
        """
        returnValue = Ciexception.objects.filter(id__in=ids).delete()
        return returnValue

    def Truncate(self):
        """
        全部清除异常
        Args:
            ids (string): 主键列表
        Returns:
            returnValue (int): 受影响行数
        """
        returnValue = Ciexception.objects.all().delete()
        return returnValue