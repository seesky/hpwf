# _*_ coding: utf-8 _*_
__author__ = 'baxuelong@163.com'
__date__ = '2018/12/11 15:33'

from django.db.utils import DatabaseError
from django.db.transaction import TransactionManagementError
from django.core.paginator import Paginator
from django.db.models import Q
from django.db import transaction

from apps.utilities.message.StatusCode import StatusCode
from apps.utilities.message.FrameworkMessage import FrameworkMessage
from apps.utilities.publiclibrary.DbCommonLibaray import DbCommonLibaray
from apps.utilities.publiclibrary.StringHelper import StringHelper
from apps.bizlogic.service.base.OrganizeService import OrganizeService

import uuid,sys
import datetime
from apps.bizlogic.models import Pistafforganize
from apps.bizlogic.models import Pistaff
from apps.bizlogic.models import Piuser
from apps.bizlogic.models import Piuserrole
from apps.bizlogic.service.base.UserService import UserSerivce
from apps.bizlogic.service.base.LogService import LogService
from apps.bizlogic.service.base.SequenceService import SequenceService

class StaffService(object):

    def Add(userInfo, entity, organizeId=""):
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
            staffOrganize.id = uuid.uuid4()
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

            LogService.WriteLog(userInfo, __class__.__name__, FrameworkMessage.StaffService,
                                sys._getframe().f_code.co_name, FrameworkMessage.StaffService_AddStaff, entity.id)

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

    def GetDT(userInfo):
        """
        获取员工列表
        Args:
        Returns:
            returnValue (List): 员工列表
        """
        LogService.WriteLog(userInfo, __class__.__name__, FrameworkMessage.StaffService,
                            sys._getframe().f_code.co_name, FrameworkMessage.StaffService_GetDT, '')
        returnValue = []
        try:
            for staff in Pistaff.objects.all():
                returnValue.append(staff)
            return returnValue
        except DatabaseError as e:
            return returnValue
        except TransactionManagementError as e:
            return returnValue

    def GetDTByPage(userInfo, searchValue, pageSize=50, order=None):
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
        LogService.WriteLog(userInfo, __class__.__name__, FrameworkMessage.StaffService,
                            sys._getframe().f_code.co_name, FrameworkMessage.StaffService_GetDTByPage, '')
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
        staffList = DbCommonLibaray.executeQuery(None, whereConditional)
        returnValue = Paginator(staffList, pageSize)
        staffCount = returnValue.count
        return staffCount,returnValue

    def GetEntity(userInfo, id):
        """
        获取员工实体
        Args:
            id (string): 员工主键
        Returns:
            returnValue (Staff or None): 员工实体
        """
        LogService.WriteLog(userInfo, __class__.__name__, FrameworkMessage.StaffService,
                            sys._getframe().f_code.co_name, FrameworkMessage.StaffService_GetEntity, id)
        try:
            staff = Pistaff.objects.get(id=id)
            return staff
        except Pistaff.DoesNotExist:
            return None

    def UpdateStaff(userInfo, entity):
        """
        更新员工
        Args:
            userEntity (Pistaff): 员工实体
        Returns:
            returnValue (string): 状态码
            returnMessage (string): 状态信息
        """
        LogService.WriteLog(userInfo, __class__.__name__, FrameworkMessage.StaffService,
                            sys._getframe().f_code.co_name, FrameworkMessage.StaffService_UpdateStaff, entity.id)
        try:
            entity.save()
            returnCode = StatusCode.statusCodeDic['OKUpdate']
            returnMessage = FrameworkMessage.MSG0010
            return returnCode, returnMessage
        except Exception as e:
            print(e)
            returnCode = StatusCode.statusCodeDic['Error']
            returnMessage = FrameworkMessage.MSG0001
            return returnCode, returnMessage

    def GetDTByIds(userInfo, ids):
        """
        按主键获取员工列表
        Args:
            ids (List[string]): 主键数组
        Returns:
            returnValue (List): 用户列表
        """
        LogService.WriteLog(userInfo, __class__.__name__, FrameworkMessage.StaffService,
                            sys._getframe().f_code.co_name, FrameworkMessage.StaffService_UpdateStaff, str(ids))
        returnValue = []
        for id in ids:
            try:
                user = Pistaff.objects.get(id=id)
                returnValue.append(user)
            except Pistaff.DoesNotExist:
                continue
        return returnValue

    def GetDTByOrganize(userInfo, organizeId, containChildren):
        """
        按组织结构获取员工列表
        Args:
            organizeId (string): 组织结构id
            containChildren (bool): 组织结构是否包含子机构
        Returns:
            returnValue (List): 员工列表
        """
        LogService.WriteLog(userInfo, __class__.__name__, FrameworkMessage.StaffService,
                            sys._getframe().f_code.co_name, FrameworkMessage.StaffService_GetDTByOrganize, organizeId)
        if containChildren:
            organizeIds = OrganizeService.GetChildrensById(None, organizeId)
            staffIds = []
            for staff in Pistafforganize.objects.filter(Q(organizeid__in=organizeIds) & Q(deletemark=0)):
                staffIds.append(staff.staffid)

            returnValue = Pistaff.objects.filter(Q(id__in=staffIds) & Q(deletemark=0)).order_by('sortcode')
            return returnValue
        else:
            starffIds = []
            for staff in Pistafforganize.objects.filter(Q(organizeid=organizeId) & Q(deletemark=0)):
                starffIds.append(staff.staffid)
            returnValue = Pistaff.objects.filter(Q(id__in=starffIds) & Q(deletemark=0)).order_by('sortcode')
            return returnValue

    def GetDTNotOrganize(userInfo):
        """
        得到未设置组织机构的员工列表
        Args:
        Returns:
            returnValue (List): 员工列表
        """
        LogService.WriteLog(userInfo, __class__.__name__, FrameworkMessage.StaffService,
                            sys._getframe().f_code.co_name, FrameworkMessage.StaffService_GetDTByOrganize, '')
        returnValue = Pistaff.objects.filter(Q(deletemark=0) & ~Q(id__in=Pistafforganize.objects.filter(Q(deletemark=0) & Q(enabled=1)).values_list('staffid', flat=True)))
        return returnValue

    def SetStaffUser(userInfo, staffId, userId):
        """
        员工关联用户
        Args:
            staffId (string): 员工主键
            userId (string): 用户主键
        Returns:
            returnValue (bool): 关联结果
        """
        LogService.WriteLog(userInfo, __class__.__name__, FrameworkMessage.StaffService,
                            sys._getframe().f_code.co_name, FrameworkMessage.StaffService_GetDTByOrganize, staffId + '/' + userId)
        try:
            if not userId:
                with transaction.atomic():
                    pistaff = Pistaff.objects.get(id=staffId)
                    pistaff.userid = userId
                    pistaff.save()
                    return True
            else:
                staffids = Pistaff.objects.filter(userid=userId)
                if len(staffids) == 0:
                    with transaction.atomic():
                        pistaff = Pistaff.objects.get(id=staffId)
                        pistaff.userid = userId
                        username = UserSerivce.GetEntity(None, userId).username
                        pistaff.username = username
                        pistaff.save()
                        return True
                else:
                    return False
        except:
            return False


    def DeleteUser(userInfo, staffId):
        """
        删除员工关联的用户
        Args:
            staffId (string): 员工主键
        Returns:
            returnValue (bool): 删除结果
        """
        LogService.WriteLog(userInfo, __class__.__name__, FrameworkMessage.StaffService,
                            sys._getframe().f_code.co_name, FrameworkMessage.StaffService_DeleteUser,
                            staffId)
        try:
            try:
                staff = Pistaff.objects.get(id = staffId)
                ids = [staff.userid]
                UserSerivce.SetDeleted(None, ids)
            except Pistaff.DoesNotExist as e:
                pass
            staff = Pistaff.objects.get(id = staffId)
            staff.userid = None
            staff.save()
            return True
        except Exception as e:
            return False

    def Delete(userInfo, id):
        """
        单个删除
        Args:
            id (string): 员工主键
        Returns:
            returnValue (bool): 删除结果
        """
        LogService.WriteLog(userInfo, __class__.__name__, FrameworkMessage.StaffService,
                            sys._getframe().f_code.co_name, FrameworkMessage.StaffService_Delete, id)
        try:
            try:
                staff = Pistaff.objects.get(id = id)
                Piuserrole.objects.filter(userid=staff.userid).delete()
                UserSerivce.Delete(None, staff.userid)
            except Pistaff.DoesNotExist as e:
                pass
            Pistafforganize.objects.filter(staffid=id).delete()
            Pistaff.objects.filter(id=id).delete()
            return True
        except Exception as e:
            return False


    def BatchDelete(userInfo, ids):
        """
        批量删除
        Args:
            ids (string[]): 员工主键列表
        Returns:
            returnValue (bool): 删除结果
        """
        LogService.WriteLog(userInfo, __class__.__name__, FrameworkMessage.StaffService,
                            sys._getframe().f_code.co_name, FrameworkMessage.StaffService_Delete, str(ids))
        try:
            try:
                UserSerivce.BatchDelete(None, Pistaff.objects.filter(id__in=ids).values_list('userid', flat=True))
                Piuserrole.objects.filter(userid__in=Pistaff.objects.filter(id__in=ids)).delete()

            except Pistaff.DoesNotExist as e:
                pass
            Pistafforganize.objects.filter(staffid__in=ids).delete()
            Pistaff.objects.filter(id__in=ids).delete()
            return True
        except Exception as e:
            return False

    def SetDeleted(userInfo, ids):
        """
        批量打删除标志
        Args:
            ids (string[]): 员工主键列表
        Returns:
            returnValue (bool): 删除结果
        """
        LogService.WriteLog(userInfo, __class__.__name__, FrameworkMessage.StaffService,
                            sys._getframe().f_code.co_name, FrameworkMessage.StaffService_SetDeleted, str(ids))
        try:
            try:
                UserSerivce.SetDeleted(None, Pistaff.objects.filter(id__in=ids).values_list('userid', flat=True))
                Piuserrole.objects.filter(userid__in=Pistaff.objects.filter(id__in=ids)).delete()
            except Pistaff.DoesNotExist as e:
                pass
            Pistafforganize.objects.filter(staffid__in=ids).update(deletemark = 1)
            Pistaff.objects.filter(id__in=ids).update(deletemark = 1)
            return True
        except Exception as e:
            return False

    def MoveTo(userInfo, id, organizeId):
        """
        移动员工数据到指定组织机构
        Args:
            id (string): 员工主键
            organizeId (string): 组织机构主键
        Returns:
            returnValue (bool): 移动结果
        """
        LogService.WriteLog(userInfo, __class__.__name__, FrameworkMessage.StaffService,
                            sys._getframe().f_code.co_name, FrameworkMessage.StaffService_MoveTo, id + '/' + organizeId)
        try:
            staff = Pistafforganize.objects.get(staffid=id)
            staff.organizeid = organizeId
            staff.save()
            return True
        except Pistafforganize.DoesNotExist as e:
            print(e)
            return False

    def BatchMoveTo(userInfo, ids, organizeId):
        """
        批量移动员工数据到指定组织机构
        Args:
            ids (string[]): 员工主键
            organizeId (string): 组织机构主键
        Returns:
            returnValue (bool): 移动结果
        """
        LogService.WriteLog(userInfo, __class__.__name__, FrameworkMessage.StaffService,
                            sys._getframe().f_code.co_name, FrameworkMessage.StaffService_MoveTo, str(ids) + '/' + organizeId)
        try:
            staff = Pistafforganize.objects.filter(staffid__in=ids).update(organizeid=organizeId)
            return True
        except Pistafforganize.DoesNotExist as e:
            print(e)
            return False
        pass

    def GetId(userInfo, valueDic):
        """
        获取主键
        Args:
            valueDic (Dic{key:value}): 参数对
        Returns:
            returnValue (string[]): ID列表
        """
        LogService.WriteLog(userInfo, __class__.__name__, FrameworkMessage.StaffService,
                            sys._getframe().f_code.co_name, FrameworkMessage.StaffService_GetId, '')
        q = Q()
        for i in valueDic:
            q.add(Q(**{i: valueDic[i]}), Q.AND)
        returnValue = Pistaff.objects.filter(q).values_list('id', flat=True)
        return returnValue