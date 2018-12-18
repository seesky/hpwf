# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2018/12/11 15:33'

from django.db.utils import DatabaseError
from django.db.transaction import TransactionManagementError
from django.core.paginator import Paginator
from django.db.models import Q

from apps.utilities.message.StatusCode import StatusCode
from apps.utilities.message.FrameworkMessage import FrameworkMessage
from apps.utilities.publiclibrary.DbCommonLibaray import DbCommonLibaray
from apps.utilities.publiclibrary.StringHelper import StringHelper
from apps.bizlogic.service.base.OrganizeService import OrganizeService

import uuid
import datetime
from apps.bizlogic.models import Pistafforganize
from apps.bizlogic.models import Pistaff

class StaffService(object):

    def Add(self, entity, organizeId=""):
        """
        添加员工
        Args:
            entity (Pistaff[]): 员工实体
        Returns:
            returnValue: 用户主键
        """
        try:
            entity.save()
            staffId = entity.id
            staffOrganize = Pistafforganize()
            staffOrganize.staffid = staffId
            staffOrganize.organizeid = organizeId
            staffOrganize.enabled = 1
            staffOrganize.deletemark = 0
            staffOrganize.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            staffOrganize.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            staffOrganize.save()
            returnCode = StatusCode.statusCodeDic['OKAdd']
            returnMessage = FrameworkMessage.MSG0009
            returnValue =  staffId
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
        获取员工列表
        Args:
        Returns:
            returnValue (List): 员工列表
        """
        returnValue = []
        try:
            for staff in Pistaff.objects.all():
                returnValue.append(staff)
            return returnValue
        except DatabaseError as e:
            return returnValue
        except TransactionManagementError as e:
            return returnValue

    def GetDTByPage(self, searchValue, pageSize=50, order=None):
        """
        分页查询
        Args:
            recordCount (int): 所有员工数
            searchValue (string): 查询字段
            pageSize (int): 每页显示
            order (string): 排序
        Returns:
            staffCount (int): 所有员工数
            returnValue (Paginator): 员工分页列表
        """
        if not searchValue:
            if not order:
                whereConditional = 'SELECT * FROM ' + Pistaff._meta.db_table + ' WHERE deletemark = 0'
            else:
                whereConditional = 'SELECT * FROM ' + Pistaff._meta.db_table + ' WHERE deletemark = 0 ORDER BY ' + order
        else:
            if not order:
                'SELECT * FROM ' + Pistaff._meta.db_table + ' WHERE ' + searchValue + ' AND deletemark = 0'
            else:
                whereConditional = 'SELECT * FROM ' + Pistaff._meta.db_table + ' WHERE ' + searchValue + ' AND deletemark = 0 ORDER BY ' + order
        staffList = DbCommonLibaray.executeQuery(self, whereConditional)
        returnValue = Paginator(staffList, pageSize)
        staffCount = returnValue.count
        return staffCount,returnValue

    def GetEntity(self, id):
        """
        获取员工实体
        Args:
            id (string): 员工主键
        Returns:
            returnValue (Staff or None): 员工实体
        """
        try:
            staff = Pistaff.objects.get(id=id)
            return staff
        except Pistaff.DoesNotExist:
            return None

    def UpdateStaff(self, entity):
        """
        更新员工
        Args:
            userEntity (Pistaff): 员工实体
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

    def GetDTByIds(self, ids):
        """
        按主键获取用户列表
        Args:
            ids (List[string]): 主键数组
        Returns:
            returnValue (List): 用户列表
        """
        returnValue = []
        for id in ids:
            try:
                user = Pistaff.objects.get(id=id)
                returnValue.append(user)
            except Pistaff.DoesNotExist:
                continue
        return returnValue

    def GetDTByOrganize(self, organizeId, containChildren):
        if containChildren:
            organizeIds = OrganizeService.GetChildrensById(self, organizeId)
            staffIds = []
            for staff in Pistafforganize.objects.filter(Q(organizeid__in=organizeIds)):
                staffIds.append(staff.staffid)

            returnValue = Pistaff.objects.filter(id__in=staffIds).order_by('sortcode')
            return returnValue
        else:
            starffIds = []
            for staff in Pistafforganize.objects.filter(Q(organizeid=organizeId)):
                starffIds.append(staff.staffid)
            print(starffIds)
            returnValue = Pistaff.objects.filter(Q(id__in=starffIds) & Q(deletemark=0)).order_by('sortcode')
            return returnValue

    def GetDTNotOrganize(self):
        pass

    def SetStaffUser(self, staffId, userId):
        pass

    def DeleteUser(self, staffId):
        pass

    def Delete(self, id):
        pass

    def BatchDelete(self, ids):
        pass

    def SetDeleted(self, ids):
        pass

    def MoveTo(self, id, organizeId):
        pass

    def BatchMoveTo(self, ids, organizeId):
        pass

    def GetId(self, name, value):
        pass