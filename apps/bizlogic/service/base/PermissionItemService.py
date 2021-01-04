# _*_ coding: utf-8 _*_
__author__ = 'baxuelong@163.com'
__date__ = '2018/12/11 17:16'

import uuid
import datetime

from django.db.models import Q
from django.db.utils import DatabaseError
from django.db.transaction import TransactionManagementError

from apps.bizlogic.models import Pipermissionitem
from apps.bizlogic.models import Pipermission
from apps.bizlogic.models import Pirole
from apps.bizlogic.models import Piuser
from apps.bizlogic.models import Piuserrole
#from apps.bizlogic.service.base.UserRoleService import UserRoleService
#from apps.bizlogic.service.base.PermissionScopeService import PermissionScopeService
from apps.utilities.message.StatusCode import StatusCode
from apps.utilities.message.FrameworkMessage import FrameworkMessage
from apps.bizlogic.models import Pipermissionscope
from apps.utilities.message.PermissionScope import PermissionScope
from apps.utilities.publiclibrary.StringHelper import StringHelper
from apps.utilities.publiclibrary.DbCommonLibaray import DbCommonLibaray


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
        permissionItemIds = PermissionItemService.GetTreeResourceScopeIds(self, userId, 'pipermissionitem', permissionItemCode, True)
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

        permissionItemIds = PermissionItemService.GetTreeResourceScopeIds(self, 'PIPERMISSIONITEM', permissionItemCode, True)
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

        list1 = Piuser.objects.filter(Q(id=userId) & Q(deletemark=0) & Q(enabled=1)).values_list('roleid', flat=True)
        list2 = Piuserrole.objects.filter(
            Q(userid=userId) & Q(roleid__in=Pirole.objects.filter(deletemark=0).values('id')) & Q(
                deletemark=0)).values_list('roleid', flat=True)
        roleIds = list1.union(list2)

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

        # Pipermissionitem.objects.get_or_create(defaults={'deletemark':'0', 'enabled':'1', 'code': permissionItemCode},
        #                                               code=permissionItemCode,
        #                                               fullname = permissionItemCode if permissionItemName else permissionItemName,
        #                                               categorycode = "Application",
        #                                               parentid = None,
        #                                               isscope = 0,
        #                                               ispublic = 0,
        #                                               allowdelete = 1,
        #                                               allowedit = 1,
        #                                               enabled = 1,
        #                                               deletemark = 0,
        #                                               moduleid = None
        #                                               )
        fullname = permissionItemCode if not permissionItemName else permissionItemName
        Pipermissionitem.objects.get_or_create(defaults={'code':permissionItemCode, 'fullname':fullname, 'categorycode':"Application", 'parentid':None, 'isscope': 0, 'ispublic' : 0, 'allowdelete' : 1, 'allowedit' : 1, 'enabled' : 1, 'deletemark' : 0, 'moduleid':None}, deletemark=0, enabled=1, code=permissionItemCode)

        item = Pipermissionitem.objects.get(Q(code=permissionItemCode) & Q(deletemark=0) & Q(enabled=1))
        return item.id

    def GetTreeResourceScopeIds(self, userId, tableName, permissionItemCode, childrens):
        """
        用户名是否重复
        Args:
            fieldNames (string): 字段名
            fieldValue (string): 字段值
        Returns:
            returnValue(bool): 已存在
        """
        resourceScopeIds = None
        resourceScopeIds = PermissionItemService.GetResourceScopeIds(self, userId, tableName, permissionItemCode)

        idList = StringHelper.ArrayToList(self, resourceScopeIds, '\'')

        if idList:
            sqlQuery = 'select id from ( select id from ' + tableName + ' where (id in (' + idList + ')) UNION ALL select ResourceTree.Id AS ID FROM ' + tableName + ' AS ResourceTree INNER JOIN pipermissionscope AS A ON A.Id = ResourceTree.ParentId) AS PermissionScopeTree'
            dataTable = DbCommonLibaray.executeQuery(self, sqlQuery)
        return resourceScopeIds

    def GetResourceScopeIds(self, userId, targetCategory, permissionItemCode):
        """
        获得用户的某个权限范围资源主键数组
        Args:
            userId (string): 用户主键
            targetCategory (string): 资源分类
            permissionItemCode (string): 权限编号
        Returns:
            returnValue(string[]): 主键数组
        """
        permissionItemId = Pipermissionitem.objects.get(code=permissionItemCode).id
        defaultRoleId = Piuser.objects.get(id=userId).roleid

        q1 = Pipermissionscope.objects.filter(Q(resourcecategory='PIUSER') & Q(resourceid=userId) & Q(targetcategory=targetCategory) & Q(permissionid=permissionItemId) & Q(enabled=1) & Q(deletemark=0)).values_list('targetid', flat=True)
        q2 = Pipermissionscope.objects.filter(Q(resourcecategory='PIROLE') & Q(resourcecategory=targetCategory) & Q(permissionid=permissionItemId) & Q(deletemark=0) & Q(enabled=1) & Q(resourceid__in=Piuserrole.objects.filter(Q(userid=userId) & Q(enabled=1) & Q(deletemark=0)).values_list('roleid', flat=True))).values_list('targetid', flat=True)
        resourceIds = q1.union(q2)

        if targetCategory == 'PIORGANIZE':
            resourceIds,permissionScope = PermissionItemService.TransformPermissionScope(None, userId, resourceIds)

        return resourceIds

    def TransformPermissionScope(self, userId, resourceIds):
        """
        转换用户的权限范围
        Args:
            userId (string): 用户主键
            resourceIds (string[]): 权限范围
        Returns:
        """
        permissionScope = PermissionScope.PermissionScopeDic.get('No')
        if len(resourceIds) > 0:
            userEntity = Piuser.objects.get(id=userId)
            for r in resourceIds:
                if r == PermissionScope.PermissionScopeDic.get('All'):
                    permissionScope = PermissionScope.PermissionScopeDic.get('All')
                    continue
                if r == PermissionScope.PermissionScopeDic.get('UserCompany'):
                    permissionScope = PermissionScope.PermissionScopeDic.get('UserCompany')
                    continue
                if r == PermissionScope.PermissionScopeDic.get('UserDepartment'):
                    permissionScope = PermissionScope.PermissionScopeDic.get('UserDepartment')
                    continue
                if r == PermissionScope.PermissionScopeDic.get('UserWorkgroup'):
                    permissionScope = PermissionScope.PermissionScopeDic.get('UserWorkgroup')
                    continue
            return resourceIds,permissionScope
        return resourceIds, permissionScope

