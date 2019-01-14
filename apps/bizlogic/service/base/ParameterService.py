# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2018/12/11 17:25'

from configobj import ConfigObj
from apps.bizlogic.models import Ciparameter
from django.db.models import Q
from apps.utilities.publiclibrary.DbCommonLibaray import DbCommonLibaray
from django.core.paginator import Paginator
import os

class ParameterService(object):



    def GetServiceConfig(key):
        """
        获取服务器上的配置信息
        Args:
            key (string): 配置项主键
        Returns:
            returnValue (string): 配置内容
        """
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config = ConfigObj(BASE_DIR + r'\..\..\utilities\config\Config.ini', encoding='UTF8')
        return config['appSettings'][key]

    def GetParameter(categoryKey, parameterId, parameterCode):
        """
        获取参数值
        Args:
            categoryKey (string): 分类键值
            parameterId (string): 参数主键
            parameterCode (string): 参数编号
        Returns:
            returnValue (string): 参数值
        """
        try:
            returnValue = Ciparameter.objects.get(Q(categorykey=categoryKey) & Q(parameterid=parameterId) & Q(parametercode=parameterCode) & Q(deletemark=0)).parametercontent
        except Ciparameter.DoesNotExist as e:
            returnValue = None
        return returnValue

    def GetEntity(self, id):
        """
        获取实体
        Args:
            id (string): 主键
        Returns:
            returnValue (Ciparameter): 配置实体
        """
        returnValue = Ciparameter.objects.get(id=id)
        return returnValue

    def SetParameter(self, categoryKey, parameterId, parameterCode, parameterContent, allowEdit=0, allowDelete=0):
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
                parameterEntity.enabled = 1
                parameterEntity.worked = 0
                parameterEntity.deletemark = 0
                parameterEntity.save()
                returnValue = 1
            return returnValue

    def GetDTByParameter(self, categoryKey, parameterId):
        """
        获取记录
        Args:
            categoryKey (string): 类别主键
            parameterId (string): 标志主键
        Returns:
            returnValue (Ciparameter[]): 数据表
        """
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

    def GetDTByPage(self, searchValue, pageSize=50, order=None):
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
        staffList = DbCommonLibaray.executeQuery(self, whereConditional)
        parameterValue = Paginator(staffList, pageSize)
        parameterCount = parameterValue.count
        return parameterCount, parameterValue

    def SetDeleted(self, id):
        """
        逻辑删除
        Args:
            id (string): 参数项主键
        Returns:
            returnValue (int): 影响行数
        """
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

    def Delete(self, id):
        """
        删除参数
        Args:
            id (string): 参数键值
        Returns:
            returnValue (int): 影响行数
        """
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