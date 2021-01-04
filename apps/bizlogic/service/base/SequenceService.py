# _*_ coding: utf-8 _*_
__author__ = 'baxuelong@163.com'
__date__ = '2018/12/11 16:22'

from apps.bizlogic.models import Cisequence
from apps.utilities.publiclibrary.DbCommonLibaray import DbCommonLibaray

from apps.utilities.message.StatusCode import StatusCode
from apps.utilities.message.FrameworkMessage import FrameworkMessage
from apps.utilities.publiclibrary.StringHelper import StringHelper
from apps.bizlogic.service.base.LogService import LogService
import sys

from django.db.utils import DatabaseError
from django.db.transaction import TransactionManagementError
from django.core.paginator import Paginator
from django.db.models import F,Q
import datetime,uuid

class SequenceService(object):
    FillZeroPrefix = True  # 是否前缀补零
    DefaultSequence = 1000  # 默认升序序列号
    DefaultReduction = 9999999  # 默认降序序列号
    DefaultPrefix = ""  # 默认的前缀
    DefaultSeparator = ""  # 默认分隔符
    DefaultStep = 1  # 递增或者递减数步调
    DefaultSequenceLength = 8  # 默认的排序码长度
    SequenceLength = 8  # 序列长度
    UsePrefix = True  # 是否采用前缀，补充0方式

    def Add(userInfo, sequenceEntity):
        """
          添加序列
          Args:
              sequenceEntity (Cisequence):
          Returns:
              returnCode(string):  状态码
              returnMessage(string):  状态信息
              returnValue（string）: 主键
        """

        LogService.WriteLog(userInfo, __class__.__name__, FrameworkMessage.SequenceService,
                            sys._getframe().f_code.co_name, FrameworkMessage.SequenceService_Add, id)

        try:
            sequenceEntity.save()
            returnCode = StatusCode.statusCodeDic['OKAdd']
            returnMessage = FrameworkMessage.MSG0009
            returnValue = sequenceEntity.id
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
        pass

    def GetDT(self):
        """
        获取序列号列表
        Args:
        Returns:
            returnValue (List): 数据表
        """
        returnValue = []
        try:
            for sequence in Cisequence.objects.filter(deletemark=0).order_by('sortcode'):
                returnValue.append(sequence)
            return returnValue
        except DatabaseError as e:
            return returnValue
        except TransactionManagementError as e:
            return returnValue

    def GetDTByPage(self, searchValue, pageSize=50, order=None):
        """
        分页查询
        Args:
            searchValue (string): 查询字段
            pageSize (int): 每页显示
            order (string): 排序
        Returns:
            staffCount (int): 所有员工数
            returnValue (Paginator): 员工分页列表
        """
        if not searchValue:
            if not order:
                whereConditional = 'SELECT * FROM ' + Cisequence._meta.db_table + ' WHERE deletemark = 0'
            else:
                whereConditional = 'SELECT * FROM ' + Cisequence._meta.db_table + ' WHERE deletemark = 0 ORDER BY ' + order
        else:
            if not order:
                'SELECT * FROM ' + Cisequence._meta.db_table + ' WHERE ' + searchValue + ' AND deletemark = 0'
            else:
                whereConditional = 'SELECT * FROM ' + Cisequence._meta.db_table + ' WHERE ' + searchValue + ' AND deletemark = 0 ORDER BY ' + order
        staffList = DbCommonLibaray.executeQuery(self, whereConditional)
        returnValue = Paginator(staffList, pageSize)
        staffCount = returnValue.count
        return staffCount,returnValue

    def GetEntity(userInfo, id):
        """
        获取实体
        Args:
            id (string): 主键
        Returns:
            returnValue (Staff or None): 实体
        """
        LogService.WriteLog(userInfo, __class__.__name__, FrameworkMessage.SequenceService,
                            sys._getframe().f_code.co_name, FrameworkMessage.SequenceService_GetEntity, id)
        try:
            sequence = Cisequence.objects.get(id=id)
            return sequence
        except Cisequence.DoesNotExist:
            return None

    def Update(self, entity):
        """
        更新序列
        Args:
            userEntity (Piuser): 序列实体
        Returns:
            returnValue (string): 状态码
            returnMessage (string): 状态信息
        """
        try:
            entity.save()
            returnCode = StatusCode.statusCodeDic['OKUpdate']
            returnMessage = FrameworkMessage.MSG0010
            return returnCode, returnMessage
        except:
            returnCode = StatusCode.statusCodeDic['Error']
            returnMessage = FrameworkMessage.MSG0001
            return returnCode, returnMessage

    def GetSequence(self, fullName):
        """
        获取序列号
        Args:
            fullName (string): 序列名称
        Returns:
            returnValue (string): 序列号
        """
        sequenceEntity = SequenceService.GetEntityByAdd(self, fullName)
        SequenceService.UpdateSequence(self, fullName, 1)
        sequence = sequenceEntity.sequence
        if SequenceService.FillZeroPrefix:
            sequence = StringHelper.RepeatString(self, '0', len(str(sequenceEntity.sequence))) + str(sequenceEntity.sequence)
        if SequenceService.UsePrefix:
            sequence = sequenceEntity.prefix + sequenceEntity.separate + sequence
        return sequence

    def GetOldSequence(self, fullName, defaultSequence, sequenceLength, fillZeroPrefix):
        """
        获取原序列号
        Args:
            fullName (string): 序列名称
            defaultSequence (int): 默认序列
            sequenceLength (int): 序列长度
            fillZeroPrefix (bool): 是否填充补零
        Returns:
            returnValue (string): 序列号
        """
        sequenceEntity = Cisequence.objects.get_or_create(defaults={'fullname': fullName}, fullname=fullName,
                                         sequence=defaultSequence,
                                         reduction=SequenceService.DefaultReduction, step=SequenceService.DefaultStep,
                                         prefix=fillZeroPrefix,
                                         separate=SequenceService.DefaultSeparator)
        sequence = sequenceEntity.sequence
        if SequenceService.FillZeroPrefix:
            sequence = StringHelper.RepeatString(self, '0', len(sequenceEntity.sequence)) + sequenceEntity.sequence
        if SequenceService.UsePrefix:
            sequence = sequenceEntity.prefix + sequenceEntity.separate + sequence
        return sequence

    def GetNewSequence(self, fullName, defaultSequence, sequenceLength, fillZeroPrefix):
        """
        获取新序列号
        Args:
            fullName (string): 序列名称
            defaultSequence (int): 默认序列
            sequenceLength (int): 序列长度
            fillZeroPrefix (bool): 是否填充补零
        Returns:
            returnValue (string): 序列号
        """
        sequenceEntity = Cisequence.objects.get_or_create(defaults={'fullname': fullName}, fullname=fullName,
                                                          sequence=defaultSequence,
                                                          reduction=SequenceService.DefaultReduction,
                                                          step=SequenceService.DefaultStep,
                                                          prefix=fillZeroPrefix,
                                                          separate=SequenceService.DefaultSeparator)
        sequence = sequenceEntity.sequence
        if SequenceService.FillZeroPrefix:
            sequence = StringHelper.RepeatString(self, '0', len(sequenceEntity.sequence)) + sequenceEntity.sequence
        if SequenceService.UsePrefix:
            sequence = sequenceEntity.prefix + sequenceEntity.separate + sequence
        return sequence

    def GetUserids(self, fullName, count):
        """
       获取序列号
       Args:
           fullName (string): 序列名称
           count (int): 个数
       Returns:
           returnValue (string): 序列号
       """
        returnValue = [count]
        sequenceEntity = SequenceService.GetEntityByAdd(self, fullName)
        SequenceService.UpdateSequence(self, fullName, count)
        sequence = sequenceEntity.sequence
        if SequenceService.FillZeroPrefix:
            sequence = StringHelper.RepeatString(self, '0', len(sequenceEntity.sequence)) + sequenceEntity.sequence
        if SequenceService.UsePrefix:
            sequence = sequenceEntity.prefix + sequenceEntity.separate + sequence
        return sequence

    def GetReduction(self, fullName):
        """
        获取倒序序列号
        Args:
            fullName (string): 序列名称
        Returns:
            returnValue (string): 序列号
        """
        #TODO：这个服务还有很多工作要做
        pass

    def Reset(self, ids):
        pass

    def Delete(userInfo, id):
        """
         删除
         Args:
             id (string): 参数项主键
         Returns:
             returnValue (int): 影响行数
         """
        LogService.WriteLog(userInfo, __class__.__name__, FrameworkMessage.SequenceService,
                            sys._getframe().f_code.co_name, FrameworkMessage.SequenceService_Delete, id)
        returnValue = Cisequence.objects.filter(id=id).delete()
        return returnValue

    def SetDeleted(userInfo, id):
        """
        逻辑删除
        Args:
            id (string): 参数项主键
        Returns:
            returnValue (int): 影响行数
        """
        LogService.WriteLog(userInfo, __class__.__name__, FrameworkMessage.SequenceService,
                            sys._getframe().f_code.co_name, FrameworkMessage.SequenceService_Delete, id)
        returnValue = Cisequence.objects.filter(id=id).update(deletemark=1)
        return returnValue

    def BatchDelete(userInfo, ids):
        """
         批量删除
         Args:
             id (string): 参数项主键
         Returns:
             returnValue (int): 影响行数
         """
        LogService.WriteLog(userInfo, __class__.__name__, FrameworkMessage.SequenceService,
                            sys._getframe().f_code.co_name, FrameworkMessage.SequenceService_Delete, id)
        returnValue = Cisequence.objects.filter(id__in=ids).delete()
        return returnValue

    def GetEntityByAdd(self, fullName):
        """
        获取添加
        Args:
            fullName (string): 序列名称
        Returns:
            returnValue (string): 序列号
        """
        id = uuid.uuid4()
        #returnValue,v = Cisequence.objects.get_or_create(defaults={'fullname':fullName}, id = id, fullname=fullName, sequence=SequenceService.DefaultSequence, reduction=SequenceService.DefaultReduction, step=SequenceService.DefaultStep, prefix=SequenceService.DefaultPrefix, separate=SequenceService.DefaultSeparator, deletemark=0, createon=datetime.datetime.now())
        returnValue, v = Cisequence.objects.get_or_create(fullname = fullName, deletemark= 0, defaults={'id':id, 'fullname':fullName, 'sequence':SequenceService.DefaultSequence, 'reduction':SequenceService.DefaultReduction, 'step':SequenceService.DefaultStep, 'prefix':SequenceService.DefaultPrefix, 'separate':SequenceService.DefaultSeparator, 'deletemark':0, 'createon':datetime.datetime.now()})
        return returnValue

    def UpdateSequence(self, fullName, sequenceCount):
        """
        获取添加
        Args:
            fullName (string): 序列名称
            sequenceCount (int): 序列个数
        Returns:
            returnValue (int): 影响行数
        """
        Cisequence.objects.filter(fullname=fullName).update(sequence=(F('sequence') + sequenceCount * F('step')))