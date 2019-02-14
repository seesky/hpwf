# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2018/12/12 8:01'

from apps.bizlogic.models import Ciitemdetails
from apps.bizlogic.models import Ciitems
from django.db.models import Q
from apps.utilities.message.StatusCode import StatusCode
from apps.utilities.message.FrameworkMessage import FrameworkMessage
from apps.bizlogic.service.base.LogService import LogService
import sys

class ItemDetailsService(object):

    def Add(userInfo, entity):
        """
        新增数据
        Args:
            entity (Ciitemdetails): 字典实体
        Returns:
            returnValue (int):
            statusMessage (stirng): 状态信息
        """
        LogService.WriteLog(userInfo, __class__.__name__, FrameworkMessage.ItemDetailsService,
                            sys._getframe().f_code.co_name, FrameworkMessage.ItemDetailsService_Add, entity.id)

        returnValue = 0
        statusMessage = ''
        if len(ItemDetailsService.GetDTByValues({'itemid':entity.itemid, 'itemname':entity.itemname, 'deletemark':0})) > 0:
            returnValue = 0
            statusMessage = "已存在相同的明细项！"
        else:
            try:
                entity.save()
                returnValue = 1
                statusMessage = "成功新增数据！"
                return returnValue,statusMessage
            except:
                returnValue = 0
                statusMessage = "操作异常！"
                return returnValue, statusMessage

    def GetDT(self):
        """
        取得列表
        Args:
        Returns:
            returnValue (Ciitemdetails[]): 字典实体列表
        """
        returnValue = Ciitemdetails.objects.filter(Q(deletemark=0)).order_by('sortcode')
        return returnValue

    def GetEntity(userInfo, id):
        """
        取得实体
        Args:
            id (string): 主键
        Returns:
            returnValue (Ciitemdetails): 字典实体
        """
        LogService.WriteLog(userInfo, __class__.__name__, FrameworkMessage.ItemDetailsService,
                            sys._getframe().f_code.co_name, FrameworkMessage.ItemDetailsService_GetEntity, id)
        try:
            returnValue = Ciitemdetails.objects.get(id = id)
            return returnValue
        except:
            returnValue = None
            return  returnValue


    def Update(entity):
        """
        更新实体
        Args:
            entity (Ciitemdetails): 实体
        Returns:
            returnCode (): 返回值
            returnMessage (): 状态码
        """
        try:
            entity.save()
            returnCode = StatusCode.statusCodeDic['OKUpdate']
            returnMessage = FrameworkMessage.MSG0010
            return returnCode,returnMessage
        except:
            returnCode = StatusCode.statusCodeDic['Error']
            returnMessage = FrameworkMessage.MSG0001
            return returnCode, returnMessage

    def GetDTByIds(ids):
        """
        根据主键列表获取实体
        Args:
            ids (string[]): 主键列表
        Returns:
            returnValue (): 返回值
        """
        returnValue = Ciitemdetails.objects.filter(Q(id__in=ids)).order_by('sortcode')
        return returnValue

    def GetDTByValues(valueDic):
        """
        按键值对获取列表
        valueDic = {key:value, key:value, ...}
        Args:
            valueDic (Dic{key:value}): 参数和值对
        Returns:
            returnValue (Pioranize[]): 角色列表
        """
        q = Q()
        for i in valueDic:
            q.add(Q(**{i: valueDic[i]}), Q.AND)
        returnValue = Ciitemdetails.objects.filter(q)
        return returnValue

    def BatchSave(entites):
        """
        批次保存数据
        Args:
            dataTable (Ciitemdetails[]): 字典列表
        Returns:
            returnValue (True or False): 保存结果
        """
        try:
            for item in entites:
                item.save()
            return True
        except:
            return False

    def Delete(id):
        """
        刪除数据
        Args:
            id (string): 主键
        Returns:
            returnValue (int): 影响行数
        """
        returnValue = Ciitemdetails.objects.filter(Q(id=id)).delete()
        return returnValue

    def BatchDelete(self, ids):
        """
        批次刪除数据
        Args:
            ids (string[]): 主键列表
        Returns:
            returnValue (int): 影响行数
        """
        returnValue = Ciitemdetails.objects.filter(Q(id__in=ids)).delete()
        return returnValue

    def SetDeleted(userInfo, ids):
        """
        批次设置删除标志
        Args:
            ids (string[]): 主键列表
        Returns:
            returnValue (int): 影响行数
        """
        LogService.WriteLog(userInfo, __class__.__name__, FrameworkMessage.ItemDetailsService,
                            sys._getframe().f_code.co_name, FrameworkMessage.ItemDetailsService_SetDeleted, str(ids))
        returnValue = Ciitemdetails.objects.filter(Q(id__in=ids)).update(deletemark=1)
        return returnValue

    def GetDTByCode(self, code):
        """
        绑定下列列表
        Args:
            code (string): Code
        Returns:
            returnValue (Item): 数据表
        """
        returnValue = Ciitemdetails.objects.filter(Q(itemid__in = Ciitems.objects.filter(code=code)) & Q(deletemark=0) & Q(enabled=1)).order_by('sortcode')
        return returnValue