# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2018/12/12 7:57'

from apps.bizlogic.models import Ciitems
from apps.bizlogic.models import Ciitemdetails
from django.db.models import Q
from apps.bizlogic.service.base.PermissionScopeService import PermissionScopeService
from apps.utilities.message.StatusCode import StatusCode
from apps.utilities.message.FrameworkMessage import FrameworkMessage
from apps.bizlogic.service.base.LogService import LogService
import sys

class ItemsService(object):

    def GetDT(userInfo):
        """
        获取列表
        Args:
        Returns:
            returnValue (CiItems):
        """
        if userInfo.IsAdministrator:
            dataTable = Ciitems.objects.filter(Q(deletemark=0)).order_by('sortcode')
        else:
            ids = PermissionScopeService.GetResourceScopeIds(None, userInfo.Id, 'ciitems', "Resource.ManagePermission")
            dataTable = Ciitems.objects.filter(Q(deletemark=0) & Q(id__in=ids)).order_by('sortcode')
        return dataTable

    def GetDTByParent(parentId):
        """
        按父节点获取列表
        Args:
            parentId (stirng): 父节点主键
        Returns:
            returnValue (CiItems[]):
        """
        returnValue = Ciitems.objects.filter(Q(deletemark=0) & Q(parentid=parentId)).order_by('sortcode')
        return returnValue

    def GetItemDetailDTByItemId(itemId):
        """
       按父节点获取列表
       Args:
           itemId (stirng): 父级主键
       Returns:
           returnValue (Ciitemdetails):
       """
        returnValue = Ciitemdetails.objects.filter(Q(deletemark=0) & Q(itemid=itemId)).order_by('sortcode')
        return returnValue

    def GetEntity(userInfo, id):
        """
       获取实体
       Args:
           id (stirng): 主键
       Returns:
           returnValue (Ciitems):
       """
        LogService.WriteLog(userInfo, __class__.__name__, FrameworkMessage.ItemsService,
                            sys._getframe().f_code.co_name, FrameworkMessage.ItemsService_GetEntity, id)
        try:
            returnValue = Ciitems.objects.get(id=id)
            return returnValue
        except:
            return None

    def Add(userInfo, itemsEntity):
        """
        新增数据
        Args:
            entity (Ciitemdetails): 字典实体
        Returns:
            returnValue (int):
            statusMessage (stirng): 状态信息
        """
        LogService.WriteLog(userInfo, __class__.__name__, FrameworkMessage.ItemsService,
                            sys._getframe().f_code.co_name, FrameworkMessage.ItemsService_Add, itemsEntity.id)
        returnValue = 0
        statusMessage = ''
        if len(Ciitems.objects.filter(Q(id=itemsEntity.id) & Q(deletemark=0))) > 0:
            returnValue = 0
            statusMessage = "已存在相同的明细项！"
        else:
            try:
                itemsEntity.save()
                returnValue = 1
                statusMessage = "成功新增数据！"
                return returnValue, statusMessage
            except:
                returnValue = 0
                statusMessage = "操作异常！"
                return returnValue, statusMessage

    def Update(userInfo, itemsEntity):
        """
        更新实体
        Args:
            entity (Ciitems): 实体
        Returns:
            returnCode (): 返回值
            returnMessage (): 状态码
        """
        LogService.WriteLog(userInfo, __class__.__name__, FrameworkMessage.ItemsService,
                            sys._getframe().f_code.co_name, FrameworkMessage.ItemsService_Update, itemsEntity.id)
        try:
            itemsEntity.save()
            returnCode = StatusCode.statusCodeDic['OKUpdate']
            returnMessage = FrameworkMessage.MSG0010
            return returnCode, returnMessage
        except:
            returnCode = StatusCode.statusCodeDic['Error']
            returnMessage = FrameworkMessage.MSG0001
            return returnCode, returnMessage

    def CreateTable(self, tableName, statusCode, statusMessage):
        pass

    def Delete(id):
        """
        根据主键删除
        Args:
            entity (Ciitems): 实体
        Returns:
            returnValue (): 返回值
        """
        returnValue = Ciitems.objects.filter(Q(id = id)).delete()
        return returnValue

    def SetDeleted(userInfo, ids):
        """
       设置删除标志
       Args:
           ids (string[]): 主键列表
       Returns:
           returnValue (): 返回值
       """
        LogService.WriteLog(userInfo, __class__.__name__, FrameworkMessage.ItemsService,
                            sys._getframe().f_code.co_name, FrameworkMessage.ItemsService_SetDeleted, str(ids))
        returnValue = Ciitems.objects.filter(Q(id__in=ids)).update(deletemark=1)
        return returnValue