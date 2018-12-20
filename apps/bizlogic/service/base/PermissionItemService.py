# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2018/12/11 17:16'

import uuid
import datetime

from django.db.models import Q
from django.db.utils import DatabaseError
from django.db.transaction import TransactionManagementError

from apps.bizlogic.models import Pipermissionitem
from apps.bizlogic.service.base.UserRoleService import UserRoleService
from apps.bizlogic.service.base.PermissionScopeService import PermissionScopeService
from apps.bizlogic.service.base.ModuleService import ModuleService
from apps.utilities.message.StatusCode import StatusCode
from apps.utilities.message.FrameworkMessage import FrameworkMessage

class PermissionItemService(object):

    def Add(self, permissionItemEntity):
        """
        添加操作权限项
        Args:
            permissionItemEntity (Pipermissionitem): 权限项实体
        Returns:
            returnCode (string): 状态码
            returnMessage (string): 状态信息
            returnValue (string): 权限项主键
        """
        try:
            permissionItemEntity.id = uuid.uuid1()
            permissionItemEntity.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            permissionItemEntity.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            permissionItemEntity.save()
            returnCode = StatusCode.statusCodeDic['OKAdd']
            returnMessage = FrameworkMessage.MSG0009
            returnValue = permissionItemEntity.id
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

    def AddByDetail(self, code, fullName):
        """
        添加操作权限项
        Args:
            permissionItemEntity (Pipermissionitem): 权限项实体
        Returns:
            returnCode (string): 状态码
            returnMessage (string): 状态信息
            returnValue (string): 权限项主键
        """
        try:
            permissionItemEntity = Pipermissionitem()
            permissionItemEntity.id = uuid.uuid1()
            permissionItemEntity.code = code
            permissionItemEntity.fullname = fullName
            permissionItemEntity.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            permissionItemEntity.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            permissionItemEntity.save()
            returnCode = StatusCode.statusCodeDic['OKAdd']
            returnMessage = FrameworkMessage.MSG0009
            returnValue = permissionItemEntity.id
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
        获取权限项列表
        Args:
        Returns:
            returnValue (PipermissionItem[]): 权限项列表
        """
        returnValue = Pipermissionitem.objects.filter(deletemark=0)
        return returnValue

    def GetList(self):
        """
        获取权限项列表
        Args:
        Returns:
            returnValue (PipermissionItem[]): 权限项列表
        """
        returnValue = Pipermissionitem.objects.filter(deletemark=0)
        return returnValue

    def GetDTByParent(self, parentId):
        """
        获取权限项列表
        Args:
        Returns:
            returnValue (PipermissionItem[]): 权限项列表
        """
        returnValue = Pipermissionitem.objects.filter(Q(parentid=parentId) & Q(deletemark=0))
        return returnValue

    def GetListByParent(self, parentId):
        """
        获取权限项列表
        Args:
            parentId: (string)
        Returns:
            returnValue (PipermissionItem[]): 权限项列表
        """
        returnValue = Pipermissionitem.objects.filter(Q(parentid=parentId) & Q(deletemark=0))
        return returnValue


    def GetDTByIds(self, ids):
        """
        按主键数组获取列表
        Args:
            ids (string[]): 主键数组
        Returns:
            returnValue (PipermissionItem[]): 权限项列表
        """
        returnValue = Pipermissionitem.objects.filter(Q(id__in=ids) & Q(deletemark=0))
        return returnValue

    def GetLicensedDT(self, userId, permissionItemCode):
        """
        获取授权范围
        Args:
            userId (string): 用户主键
            permissionItemCode (string): 权限代码
        Returns:
            returnValue (PipermissionItem[]): 权限项列表
        """
        permissionItemId = Pipermissionitem.objects.get(Q(deletemark=0) & Q(code='Resource.ManagePermission')).id
        #这里需要判断,是系统权限？
        isRole = False
        isRole = UserRoleService.UserInRole(self, userId, 'UserAdmin')
        if(isRole):
            returnValue = Pipermissionitem.objects.filter(Q(categorycode='System') & Q(deletemark=0) & Q(enabled=1)).order_by('sortcode')
            return returnValue
        isRole = UserRoleService.UserInRole(self, userId, 'Admin')
        if(isRole):
            returnValue = Pipermissionitem.objects.filter(
                Q(categorycode='Application') & Q(deletemark=0) & Q(enabled=1)).order_by('sortcode')
            return returnValue
        permissionItemIds = PermissionScopeService.GetTreeResourceScopeIds(self, userId, 'pipermissionitem', permissionItemCode, True)
        returnValue = Pipermissionitem.objects.filter(
            Q(id__in=permissionItemIds) & Q(deletemark=0) & Q(enabled=1)).order_by('sortcode')
        return returnValue


    def GetEntity(self, id):
        """
        获取权限项实体
        Args:
            id (string): 权限项主键
        Returns:
            returnValue (PipermissionItem): 权限项实体
        """
        try:
            returnValue = Pipermissionitem.objects.get(id=id)
            return returnValue
        except Pipermissionitem.DoesNotExist as e:
            return None

    def GetEntityByCode(self, code):
        """
        按编号获取权限项实体
        Args:
            code (string): 权限项编号
        Returns:
            returnValue (PipermissionItem): 权限项实体
        """
        try:
            returnValue = Pipermissionitem.objects.get(code=code)
            return returnValue
        except Pipermissionitem.DoesNotExist as e:
            return None

    def Update(self, permissionItemEntity):
        """
        更新权限项
        Args:
            userEntity (Piuser): 用户实体
        Returns:
            returnValue (string): 状态码
            returnMessage (string): 状态信息
        """
        try:
            permissionItemEntity.save()
            returnCode = StatusCode.statusCodeDic['OKUpdate']
            returnMessage = FrameworkMessage.MSG0010
            return returnCode, returnMessage
        except:
            returnCode = StatusCode.statusCodeDic['Error']
            returnMessage = FrameworkMessage.MSG0001
            return returnCode, returnMessage

    def MoveTo(self, permissionItemId, parentId):
        """
        移动权限项
        Args:
            permissionItemId (string): 权限项主键
            parentId (string): 更改后的父节点主键
        Returns:
            returnValue (True or False): 保存结果
        """
        try:
            organize = Pipermissionitem.objects.get(id=permissionItemId)
            organize.parentid = parentId
            organize.save()
            return True
        except Pipermissionitem.DoesNotExist:
            return False

    def BatchMoveTo(self, permissionItemIds, parentId):
        """
        批量移动权限项
        Args:
            permissionItemIds (string): 权限项主键列表
            parentId (string): 更改后的父节点主键
        Returns:
            returnValue (True or False): 保存结果
        """
        try:
            organize = Pipermissionitem.objects.filter(id__in=permissionItemIds).update(parentid=parentId)
            return True
        except:
            return False

    def Delete(self, id):
        """
        删除权限项
        Args:
            id (string): 权限项主键
        Returns:
            returnValue (True or False): 删除结果
        """
        try:
            try:
                organize = Pipermissionitem.objects.get(id=id)
            except Pipermissionitem.DoesNotExist as e:
                return False
            organize.deletemark = 1
            organize.save()
            return True
        except Exception as e:
            return False

    def BatchDelete(self, ids):
        """
        批量删除权限项
        Args:
            ids (string): 权限项主键列表
        Returns:
            returnValue (True or False): 删除结果
        """
        try:
            organize = Pipermissionitem.objects.filter(id__in=ids).update(deletemark=1)
            return True
        except Exception as e:
            return False

    def SetDeleted(self, ids):
        """
        批量打删除标志
        Args:
            ids (string): 权限项主键列表
        Returns:
            returnValue (True or False): 删除结果
        """
        try:
            organize = Pipermissionitem.objects.filter(id__in=ids).update(deletemark=1)
            return True
        except Exception as e:
            return False

    def BatchSave(self, dataTable):
        """
        批量保存实体
        Args:
            dataTable (Pipermissionitem[]): 权限项实体列表
        Returns:
            returnValue (True or False): 保存结果
        """

        try:
            for item in dataTable:
                item.save()
            return True
        except:
            return False

    def BatchSetSortCode(self, ids):
        """
        重新生成排序码
        Args:
            ids (string[]): 权限项实体列表
        Returns:
            returnValue (True or False): 保存结果
        """
        pass

    def GetIdsByModule(self, moduleId):
        """
        得到指定模块的操作权限主健数组
        Args:
            moduleId (string): 权限项实体列表
        Returns:
            returnValue (string[]): 主键数组
        """
        returnValue = ModuleService.GetPermissionIds(self, moduleId)
        return returnValue