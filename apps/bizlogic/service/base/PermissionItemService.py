# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2018/12/11 17:16'

import uuid
import datetime

from django.db.models import Q
from django.db.utils import DatabaseError
from django.db.transaction import TransactionManagementError

from apps.bizlogic.models import Pipermissionitem
from apps.bizlogic.models import Pipermission
from apps.bizlogic.models import Pirole
#from apps.bizlogic.service.base.UserRoleService import UserRoleService
from apps.bizlogic.service.base.PermissionScopeService import PermissionScopeService
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
        returnValue = Pipermissionitem.objects.filter(deletemark=0).order_by('sortcode')
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
        returnValue = Pipermissionitem.objects.filter(Q(id__in=ids) & Q(deletemark=0)).order_by('sortcode')
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
        isRole = PermissionItemService.UserInRole(self, userId, 'UserAdmin')
        if(isRole):
            returnValue = Pipermissionitem.objects.filter(Q(categorycode='System') & Q(deletemark=0) & Q(enabled=1)).order_by('sortcode')
            return returnValue
        isRole = PermissionItemService.UserInRole(self, userId, 'Admin')
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
        returnValue = Pipermission.objects.filter(Q(resourcecategory='PIMODULE') & Q(resourceid=moduleId) & Q(deletemark=0))
        return returnValue

    def GetDTByUser(self, userId, permissionItemCode):
        # 这里需要判断,是系统权限？
        isRole = False
        irRole = PermissionItemService.UserInRole(self, userId, "UserAdmin")
        # 用户管理员
        if isRole:
            returnValue = Pipermissionitem.objects.filter(Q(categorycode='System') & Q(deletemark=0) & Q(enabled=1)).order_by(
                'sortcode')
            return returnValue

        isRole = PermissionItemService.UserInRole(self, userId, "Admin")
        if isRole:
            returnValue = Pipermissionitem.objects.filter(Q(categorycode='Application') & Q(deletemark=0) & Q(enabled=1)).order_by(
                'sortcode')
            return returnValue

        permissionItemIds = PermissionScopeService.GetTreeResourceScopeIds(self, 'PIPERMISSIONITEM', permissionItemCode, True)
        returnValue = Pipermissionitem.objects.filter(Q(id__in=permissionItemIds) & Q(deletemark=0) & Q(enabled=1))
        return returnValue

    def UserInRole(self, userId, roleCode):
        """
        用户是否在某个角色里的判断
        Args:
            userId (string): 用户ID
            roleCode (string): 角色编号
        Returns:
            returnValue (Pirole[]): 角色列表
        """
        returnValue = False
        if not roleCode:
            return False
        roleId = Pirole.objects.get(Q(deletemark=0) & Q(code=roleCode)).id
        if not roleId:
            return False
        roleIds = UserRoleService.GetAllRoleIds(self, userId)
        if roleId in roleIds:
            return True
        else:
            return False

    def GetId(self, permissionScopeCode):
        try:
            id = Pipermissionitem.objects.get(code = permissionScopeCode).id
            return id
        except Pipermissionitem.DoesNotExist as e:
            return None

    def GetIdByAdd(permissionItemCode, permissionItemName = None):
        """
        获取一个操作权限的主键,若不存在就自动增加一个
        Args:
            permissionItemCode (string): 操作权限编号
            permissionItemName (string): 操作权限名称
        Returns:
            returnValue (int): 主键
        """
        #判断当前判断的权限是否存在，否则很容易出现前台设置了权限，后台没此项权限
        #需要自动的能把前台判断过的权限，都记录到后台来

        Pipermissionitem.objects.get_or_create(defaults={'deletemark':'0', 'enabled':'1', 'code': permissionItemCode},
                                                      code=permissionItemCode,
                                                      fullname = permissionItemCode if permissionItemName else permissionItemName,
                                                      categorycode = "Application",
                                                      parentid = None,
                                                      isscope = 0,
                                                      ispublic = 0,
                                                      allowdelete = 1,
                                                      allowedit = 1,
                                                      enabled = 1,
                                                      deletemark = 0,
                                                      moduleid = None
                                                      )

        item = Pipermissionitem.objects.get(Q(code=permissionItemCode) & Q(deletemark=0) & Q(enabled=1))
        return item.id