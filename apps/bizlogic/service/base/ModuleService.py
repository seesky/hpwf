# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2018/12/11 15:55'

from apps.bizlogic.models import Pipermission

from django.db.models import Q
from django.db.utils import DatabaseError
from django.db.transaction import TransactionManagementError
from apps.bizlogic.models import Pimodule
from apps.utilities.publiclibrary.DbCommonLibaray import DbCommonLibaray
from apps.utilities.message.StatusCode import StatusCode
from apps.utilities.message.FrameworkMessage import FrameworkMessage
from apps.bizlogic.service.permission.ModulePermission import ModulePermission
from apps.bizlogic.service.base.PermissionItemService import PermissionItemService
from apps.bizlogic.service.base.PermissionScopeService import PermissionScopeService

class ModuleService(object):
    def GetDT(self):
        """
        获取模块列表
        Args:
        Returns:
            returnValue (Pimodule[]): 模块实体
        """
        returnValue = Pimodule.objects.filter(deletemark=0).order_by('sortcode')
        return returnValue

    def GetDTByCondition(self, condition):
        """
        通过条件得到模块
        Args:
            condition (string): 条件表达式
        Returns:
            returnValue (Pimodule[]): 模块实体
        """
        if not condition:
            condition = ' deletemark=0 '
        else:
            condition = condition + ' AND deletemark = 0'
        returnValue = DbCommonLibaray.executeQuery(self, condition)
        return returnValue

    def GetList(self):
        """
        获取模块列表
        Args:
        Returns:
            returnValue (Pimodule[]): 模块实体
        """
        returnValue = Pimodule.objects.filter(deletemark=0).order_by('sortcode')
        return returnValue

    def GetDTByIds(self, ids):
        """
        按主键数组获取列表
        Args:
            ids (string[]): 主键列表
        Returns:
            returnValue (Pimodule[]): 模块实体列表
        """
        returnValue = Pimodule.objects.filter(Q(deletemark=0) & Q(id__in=ids)).order_by('sortcode')
        return returnValue

    def GetEntity(self, id):
        """
        按主键数组获取列表
        Args:
            id (string): 主键
        Returns:
            returnValue (Pimodule or None): 模块实体
        """
        try:
            returnValue = Pimodule.objects.get(id=id)
        except Pimodule.DoesNotExist as e:
            returnValue = None
        return returnValue

    def GetFullNameByCode(self, code):
        """
        通过编号获取模块名称
        Args:
            code (string): 编号
        Returns:
            returnValue (string or None): 模块名称
        """
        try:
            module = Pimodule.objects.get(code=code)
            returnValue = module.fullname
            return returnValue
        except Pimodule.DoesNotExist as e:
            return None

    def Add(self, moduleEntity):
        """
        添加模块菜单
        Args:
            moduleEntity (Pimodule): 模块实体
        Returns:
            returnCode: 状态码
            returnMessage: 状态信息
            returnValue: 主键
        """
        if len(moduleEntity.code) > 0 & ModuleService.Exists(self, moduleEntity):
            try:

                moduleEntity.save()
                returnCode = StatusCode.statusCodeDic['OKAdd']
                returnMessage = FrameworkMessage.MSG0009
                returnValue = moduleEntity.id
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
        else:
            returnCode = StatusCode.statusCodeDic['ErrorCodeExist']
            returnValue = None
            returnMessage = FrameworkMessage.MSG0001
            return returnCode, returnMessage, returnValue

    def Update(self, moduleEntity):
        """
        更新模块菜单
        Args:
            moduleEntity (Pimodule): 模块实体
        Returns:
            returnCode: 状态码
            returnValue: 主键
        """
        # returnValue = 0
        # if len(moduleEntity.code) > 0 & ModuleService.Exists(self, moduleEntity):
        #     statusCode = StatusCode.statusCodeDic['ErrorCodeExist']  #17
        # else:
        #     try:
        #         moduleEntity.save()
        #         returnValue = statusCode = 1
        #         return statusCode,returnValue
        #     except:
        #         returnValue = statusCode = 0
        #         return statusCode, returnValue
        try:
            moduleEntity.save()
            returnCode = StatusCode.statusCodeDic['OKUpdate']
            returnMessage = FrameworkMessage.MSG0010
            return returnCode, returnMessage
        except:
            returnCode = StatusCode.statusCodeDic['OKUpdate']
            returnMessage = FrameworkMessage.MSG0010
            return returnCode, returnMessage



    def GetDTByParent(self, parentId):
        """
        按父节点获得列表
        Args:
            parentId (string): 父结点主键
        Returns:
            returnValue (Pimodule[]): 模块实体列表
        """
        returnValue = Pimodule.objects.filter(Q(deletemark=0) & Q(parentid=parentId)).order_by('sortcode')
        return returnValue

    def Delete(self, id):
        """
        删除模块
        Args:
            id (string): 主键
        Returns:
            returnValue (True or False): 删除结果
        """
        try:
            try:
                module = Pimodule.objects.get(id=id)
            except Pimodule.DoesNotExist as e:
                return False
            module.deletemark = 1
            module.save()
            return True
        except Exception as e:
            return False

    def BatchDelete(self, ids):
        """
        批量删除模块
        Args:
            ids (string): 主键数组
        Returns:
            returnValue (True or False): 删除结果
        """
        try:
            organize = Pimodule.objects.filter(id__in=ids).update(deletemark=1)
            return True
        except Exception as e:
            return False

    def SetDeleted(self, ids):
        """
        批量打删除标志
        Args:
            ids (string): 主键数组
        Returns:
            returnValue (True or False): 删除结果
        """
        try:
            organize = Pimodule.objects.filter(id__in=ids).update(deletemark=1)
            return True
        except Exception as e:
            return False

    def MoveTo(self, moduleId, parentId):
        """
        移动模块
        Args:
            permissionItemId (string): 权限项主键
            parentId (string): 更改后的父节点主键
        Returns:
            returnValue (True or False): 移动结果
        """
        try:
            module = Pimodule.objects.get(id=moduleId)
            module.parentid = parentId
            module.save()
            return True
        except Pimodule.DoesNotExist:
            return False

    def BatchMoveTo(self, moduleIds, parentId):
        """
        批量移动权限项
        Args:
            permissionItemIds (string): 权限项主键列表
            parentId (string): 更改后的父节点主键
        Returns:
            returnValue (True or False): 保存结果
        """
        try:
            module = Pimodule.objects.filter(id__in=moduleIds).update(parentid=parentId)
            return True
        except:
            return False

    def BatchSave(self, dataTable):
        """
        批量进行保存
        Args:
            dataTable (Pimodule[]): 实体列表
        Returns:
            returnValue (True or False): 保存结果
        """
        try:
            for module in dataTable:
                module.save()
            return True
        except:
            return False

    def SetSortCode(self, ids):

        pass

    def GetPermissionDT(self, moduleId):
        """
        获取关联的权限项列表
        Args:
            moduleId (string): 主键
        Returns:
            returnValue (Pimodule): 模块实体列表
        """
        ids = ModulePermission.GetPermissionIds(self, moduleId)
        returnValue = PermissionItemService.GetDTByIds(self, ids)
        return returnValue

    def GetIdsByPermission(self, permissionItemId):
        """
        获取菜单主健数组
        Args:
            permissionItemId (string): 权限项主键
        Returns:
            returnValue (string[]): 模块主键数组
        """
        returnValue = ModulePermission.GetModuleIds(self, permissionItemId)
        return returnValue

    def BatchAddPermissions(self, moduleId, permissionItemIds):
        """
        模块批量关联操作权限项
        Args:
            moduleId (string): 模块主键
            permissionItemIds (string): 权限项主键
        Returns:
            returnValue (bool): 关联结果
        """
        returnValue = ModulePermission.AddsI(self, moduleId, permissionItemIds)
        pass

    def BatchAddModules(self, moduleIds, permissionItemId):
        """
        操作权限项关联模块菜单
        Args:
            moduleIds (string): 模块主键列表
            permissionItemId (string): 权限项主键
        Returns:
            returnValue (bool): 关联结果
        """
        returnValue = ModulePermission.AddsM(self, moduleIds, permissionItemId)
        return returnValue

    def BatchDeletePermissions(self, moduleId, permissionItemIds):
        """
        撤销模块菜单与操作权限项的关联
        Args:
            moduleIds (string): 模块主键列表
            permissionItemId (string): 权限项主键
        Returns:
            returnValue (bool): 删除关联结果
        """
        returnValue = ModulePermission.DeletesI(self, moduleId, permissionItemIds)
        return returnValue

    def BatchDeleteModules(self, modulesIds, permissionItemId):
        """
        撤销操作权限项与模块菜单的关联
        Args:
            moduleId (string): 模块主键
            permissionItemIds (string): 权限项主键
        Returns:
            returnValue (bool): 删除关联结果
        """
        returnValue = ModulePermission.DeletesM(self, modulesIds, permissionItemId)
        return returnValue

    def GetPermissionIds(self, moduleId):
        returnValue = Pipermission.objects.filter(Q(resourcecategory='PIMODULE') & Q(resourceid=moduleId) & Q(deletemark=0))
        return returnValue

    def Exists(self, entity):
        try:
            Pimodule.objects.get(Q(deletemark=0) & Q(code=entity.code) & Q(fullname=entity.fullname) & Q(id=entity.id))
            return True
        except Pimodule.DoesNotExist as e:
            return False


    def GetIDsByUser(self, userId):
        """
        获取用户有权限访问的模块主键
        Args:
            userId (string): 用户主键
        Returns:
            returnValue (string[]): 主键列表
        """
        #公开的模块谁都可以访问
        openModuleIds = Pimodule.objects.filter(Q(ispublic=1) & Q(enabled=1) & Q(deletemark=0)).values_list('id', flat=True)
        #非公开的模块
        if userId:
            #模块访问，连同用户本身的，还有角色的，全部获取出来
            permissionItemCode = 'Resource.AccessPermission'
            otherModuleIds = PermissionScopeService.GetResourceScopeIds(self, userId, 'PIMODULE', permissionItemCode)

        return openModuleIds.union(otherModuleIds)


    def GetDTByUser(self, userId):
        """
        某个用户可以访问的所有菜单列表
        Args:
            userId (string): 用户主键
        Returns:
            returnValue (Pimodule): 数据表
        """
        moduleIds = ModuleService.GetIDsByUser(self, userId)
        return ModuleService.GetDTByIds(self, moduleIds)
