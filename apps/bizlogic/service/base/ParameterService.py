# _*_ coding: utf-8 _*_
__author__ = 'baxuelong@163.com'
__date__ = '2018/12/11 17:25'

from configobj import ConfigObj
from apps.bizlogic.models import Ciparameter
from django.db.models import Q
from apps.utilities.publiclibrary.DbCommonLibaray import DbCommonLibaray
from django.core.paginator import Paginator
import os,sys
from apps.utilities.message.StatusCode import StatusCode
from apps.utilities.message.FrameworkMessage import FrameworkMessage
from django.db.utils import DatabaseError
from django.db.transaction import TransactionManagementError
from apps.bizlogic.service.base.LogService import LogService
import datetime

class ParameterService(object):



    def GetServiceConfig(userInfo, key):
        """
        获取服务器上的配置信息
        Args:
            key (string): 配置项主键
        Returns:
            returnValue (string): 配置内容
        """
        if userInfo:
            LogService.WriteLog(userInfo, __class__.__name__, FrameworkMessage.ParameterService,
                            sys._getframe().f_code.co_name, FrameworkMessage.ParameterService_GetServiceConfig, id)
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config = ConfigObj(BASE_DIR + r'\..\..\utilities\config\Config.ini', encoding='UTF8')
        return config['appSettings'][key]

    def GetParameter(userInfo, categoryKey, parameterId, parameterCode):
        """
        获取参数值
        Args:
            categoryKey (string): 分类键值
            parameterId (string): 参数主键
            parameterCode (string): 参数编号
        Returns:
            returnValue (string): 参数值
        """
        LogService.WriteLog(userInfo, __class__.__name__, FrameworkMessage.ParameterService,
                            sys._getframe().f_code.co_name, FrameworkMessage.ParameterService_GetParameter, id)
        try:
            returnValue = Ciparameter.objects.get(Q(categorykey=categoryKey) & Q(parameterid=parameterId) & Q(parametercode=parameterCode) & Q(deletemark=0)).parametercontent
        except Ciparameter.DoesNotExist as e:
            returnValue = None
        return returnValue

    def GetEntity(userInfo, id):
        """
        获取实体
        Args:
            id (string): 主键
        Returns:
            returnValue (Ciparameter): 配置实体
        """
        LogService.WriteLog(userInfo, __class__.__name__, FrameworkMessage.ParameterService,
                            sys._getframe().f_code.co_name, FrameworkMessage.ParameterService_GetEntity, id)
        try:
            returnValue = Ciparameter.objects.get(id=id)
            return returnValue
        except Ciparameter.DoesNotExist:
            return None

    def SetParameter(userInfo, categoryKey, parameterId, parameterCode, parameterContent, allowEdit=0, allowDelete=0):
        """
        设置参数值
        Args:
            categoryKey (string): 分类键值
            parameterId (string): 参数主键
            parameterCode (string): 参数编号
            parameterContent (string): 参数内容
            allowEdit (int): 允许编辑
            allowDelete (int): 允许删除
        Returns:
            returnValue (int): 影响行数
        """
        LogService.WriteLog(userInfo, __class__.__name__, FrameworkMessage.ParameterService,
                            sys._getframe().f_code.co_name, FrameworkMessage.ParameterService_SetParameter, id)

        returnValue = 0
        if not parameterContent:
            returnValue = Ciparameter.objects.filter(Q(categorykey=categoryKey) & Q(parameterid=parameterId) & Q(parametercode=parameterCode) & Q(deletemark=0)).delete()
        else:
            returnValue = Ciparameter.objects.filter(Q(categorykey=categoryKey) & Q(parameterid=parameterId) & Q(parametercode=parameterCode) & Q(deletemark=0)).update(parametercontent=parameterContent)
            if returnValue == 0:
                parameterEntity = Ciparameter()
                parameterEntity.categorykey = categoryKey
                parameterEntity.parameterid = parameterId
                parameterEntity.parametercode = parameterCode
                parameterEntity.parametercontent = parameterContent
                parameterEntity.allowdelete = allowDelete
                parameterEntity.allowedit = allowEdit
                parameterEntity.createon = datetime.datetime.now()
                parameterEntity.modifiedon = parameterEntity.createon
                parameterEntity.enabled = 1
                parameterEntity.worked = 0
                parameterEntity.deletemark = 0
                parameterEntity.save()
                returnValue = 1
            return returnValue

    def GetDTByParameter(userInfo, categoryKey, parameterId):
        """
        获取记录
        Args:
            categoryKey (string): 类别主键
            parameterId (string): 标志主键
        Returns:
            returnValue (Ciparameter[]): 数据表
        """
        LogService.WriteLog(userInfo, __class__.__name__, FrameworkMessage.ParameterService,
                            sys._getframe().f_code.co_name, FrameworkMessage.ParameterService_GetDTByParameter, parameterId)
        returnValue = Ciparameter.objects.filter(Q(categorykey=categoryKey) & Q(parameterid=parameterId) & Q(deletemark=0))
        return returnValue

    def GetListByParameter(self, categoryKey, parameterId):
        """
        获取记录
        Args:
            categoryKey (string): 类别主键
            parameterId (string): 标志主键
        Returns:
            returnValue (Ciparameter[]): 数据表
        """
        returnValue = Ciparameter.objects.filter(
            Q(categorykey=categoryKey) & Q(parameterid=parameterId) & Q(deletemark=0))
        return returnValue

    def GetDTByParameterCode(self, categoryKey, parameterId, parameterCode):
        """
        按编号获取参数列表
        Args:
            categoryKey (string): 类别主键
            parameterId (string): 参数主键
            parameterCode (string): 参数编号
        Returns:
            returnValue (Ciparameter[]): 数据表
        """
        returnValue = Ciparameter.objects.filter(Q(categorykey=categoryKey) & Q(parameterid=parameterId) & Q(deletemark=0) & Q(parametercode=parameterCode))
        return returnValue

    def GetListByParameterCode(self, categoryKey, parameterId, parameterCode):
        """
        按编号获取参数列表
        Args:
            categoryKey (string): 类别主键
            parameterId (string): 参数主键
            parameterCode (string): 参数编号
        Returns:
            returnValue (Ciparameter[]): 数据表
        """
        returnValue = Ciparameter.objects.filter(
            Q(categorykey=categoryKey) & Q(parameterid=parameterId) & Q(deletemark=0) & Q(parametercode=parameterCode))
        return returnValue

    def GetDTByPage(userInfo, searchValue, pageSize=50, order=None):
        """
        分页查询
        Args:
            searchValue (string): 查询字段
            pageSize (int): 每页显示
            order (string): 排序
        Returns:
            staffCount (int): 所有参数数量
            returnValue (Paginator): 参数分页列表
        """
        LogService.WriteLog(userInfo, __class__.__name__, FrameworkMessage.ParameterService,
                            sys._getframe().f_code.co_name, FrameworkMessage.ParameterService_GetDTByPage,
                            '')
        if not searchValue:
            if not order:
                whereConditional = 'SELECT * FROM ' + Ciparameter._meta.db_table + ' WHERE deletemark = 0'
            else:
                whereConditional = 'SELECT * FROM ' + Ciparameter._meta.db_table + ' WHERE deletemark = 0 ORDER BY ' + order
        else:
            if not order:
                'SELECT * FROM ' + Ciparameter._meta.db_table + ' WHERE ' + searchValue + ' AND deletemark = 0'
            else:
                whereConditional = 'SELECT * FROM ' + Ciparameter._meta.db_table + ' WHERE ' + searchValue + ' AND deletemark = 0 ORDER BY ' + order
        staffList = DbCommonLibaray.executeQuery(None, whereConditional)
        parameterValue = Paginator(staffList, pageSize)
        parameterCount = parameterValue.count
        return parameterCount, parameterValue

    def SetDeleted(userInfo, id):
        """
        逻辑删除
        Args:
            id (string): 参数项主键
        Returns:
            returnValue (int): 影响行数
        """
        LogService.WriteLog(userInfo, __class__.__name__, FrameworkMessage.ParameterService,
                            sys._getframe().f_code.co_name, FrameworkMessage.ParameterService_SetDeleted, id)
        returnValue = Ciparameter.objects.filter(id=id).update(deletemark=1)
        return returnValue

    def DeleteByParameter(self, categoryKey, parameterId):
        """
        删除参数
        Args:
            categoryKey (string): 分类键值
            parameterId (string): 参数主键
        Returns:
            returnValue (int): 影响行数
        """
        returnValue = Ciparameter.objects.filter(Q(categorykey=categoryKey) & Q(parameterid=parameterId)).delete()
        return returnValue

    def DeleteByParameterCode(self, categoryKey, parameterId, parameterCode):
        """
        按参数编号删除
        Args:
            categoryKey (string): 分类键值
            parameterId (string): 参数主键
            parameterCode (string): 参数编号
        Returns:
            returnValue (int): 影响行数
        """
        returnValue = Ciparameter.objects.filter(Q(categorykey=categoryKey) & Q(parameterid=parameterId) & Q(parametercode=parameterCode)).delete()
        return returnValue

    def Delete(userInfo, id):
        """
        删除参数
        Args:
            id (string): 参数键值
        Returns:
            returnValue (int): 影响行数
        """
        LogService.WriteLog(userInfo, __class__.__name__, FrameworkMessage.ParameterService,
                            sys._getframe().f_code.co_name, FrameworkMessage.ParameterService_Add, id)
        returnValue = Ciparameter.objects.filter(id=id).delete()
        return returnValue

    def BatchDelete(self, ids):
        """
        删除参数
        Args:
            id (string): 参数键值
        Returns:
            returnValue (int): 影响行数
        """
        returnValue = Ciparameter.objects.filter(id__in=ids).delete()
        return returnValue

    def Exists(self, parameterId, categoryKey):
        """
        判断参数是否存在
        Args:
            parameterId (string): 参数键值
            categoryKey (string): 分类键值
        Returns:
            returnValue (True or False): 是否存在
        """
        try:
            Ciparameter.objects.get(Q(parameterid=parameterId) & Q(categorykey=categoryKey))
            return True
        except Ciparameter.DoesNotExist as e:
            return False

    def Add(userInfo, parameterEntity):
        """
        添加模块菜单
        Args:
            parameterEntity (Ciparameter): 参数实体
        Returns:
            returnCode: 状态码
            returnMessage: 状态信息
            returnValue: 主键
        """
        LogService.WriteLog(userInfo, __class__.__name__, FrameworkMessage.ParameterService, sys._getframe().f_code.co_name, FrameworkMessage.ParameterService_Add, parameterEntity.id)
        try:
            parameterEntity.save()
            returnCode = StatusCode.statusCodeDic['OKAdd']
            returnMessage = FrameworkMessage.MSG0009
            returnValue = parameterEntity.id
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

    def Update(userInfo, parameterEntity):
        """
        更新模块菜单
        Args:
            parameterEntity (Ciparameter): 模块实体
        Returns:
            returnCode: 状态码
            returnValue: 主键
        """
        LogService.WriteLog(userInfo, __class__.__name__, FrameworkMessage.ParameterService,
                            sys._getframe().f_code.co_name, FrameworkMessage.ParameterService_Update, parameterEntity.id)
        try:
            parameterEntity.save()
            returnCode = StatusCode.statusCodeDic['OKUpdate']
            returnMessage = FrameworkMessage.MSG0010
            return returnCode, returnMessage
        except:
            returnCode = StatusCode.statusCodeDic['OKUpdate']
            returnMessage = FrameworkMessage.MSG0010
            return returnCode, returnMessage