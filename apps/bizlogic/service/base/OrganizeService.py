# _*_ coding: utf-8 _*_
__author__ = 'baxuelong@163.com'
__date__ = '2018/12/11 14:25'

from django.db.utils import DatabaseError
from django.db.transaction import TransactionManagementError
from django.db.models import Q

from apps.bizlogic.models import Piorganize
from apps.bizlogic.models import Piuser
from apps.bizlogic.models import Pistaff
from apps.bizlogic.models import Pistafforganize

from apps.utilities.message.StatusCode import StatusCode
from apps.utilities.message.FrameworkMessage import FrameworkMessage
from apps.utilities.publiclibrary.DbCommonLibaray import DbCommonLibaray
from apps.utilities.publiclibrary.SystemInfo import SystemInfo

import datetime

class OrganizeService(object):
    # 内部组织机构表
    InnerOrganizeDT = None

    # 最后检查组织机构时间
    LastCheckOrgTime = datetime.datetime.min

    # 在线状态表
    OnLineStateDT = None

    def Add(self, entity):
        """
        添加组织
        Args:
            entity (Piorganize): 组织实体
        Returns:
            returnValue: 组织主键
        """
        try:
            entity.save()
            returnCode = StatusCode.statusCodeDic['OKAdd']
            returnMessage = FrameworkMessage.MSG0009
            returnValue = entity.id
            return returnCode, returnMessage, returnValue
        except DatabaseError as e:
            returnCode = StatusCode.statusCodeDic['DbError']
            returnMessage = FrameworkMessage.MSG0001
            returnValue = None
            return returnCode, returnMessage, returnValue
        except TransactionManagementError as e:
            returnCode = StatusCode.statusCodeDic['DbError']
            returnMessage = FrameworkMessage.MSG0001
            returnValue = None
            return returnCode, returnMessage, returnValue

    def BatchDelete(self, ids):
        """
        批量物理删除组织机构
        Args:
            ids (string[]): 组织机构主键
        Returns:
            returnValue (True or False): 删除结果
        """
        try:
            # 已删除组织机构Piorganize表中的DELETEMARK设置为1
            organize = Piorganize.objects.filter(id__in=ids).update(deletemark = 1)
            return True
        except Exception as e:
            print(e)
            return False

    def BatchMoveTo(self, organizeIds, parentId):
        """
        批量移动组织机构
        Args:
            organizeIds (string): 组织结构主键
            parentId (string): 更改后的父节点主键
        Returns:
            returnValue (True or False): 保存结果
        """
        try:
            Piorganize.objects.filter(id__in=organizeIds).update(parentid=parentId)
            return True
        except Exception as e:
            print(e)
            return False

    def BatchSave(self, dataTable):
        """
        批量保存
        Args:
            dataTable (Piorganize[]): 组织结构列表
        Returns:
            returnValue (True or False): 保存结果
        """
        try:
            for organize in dataTable:
                organize.save()
            return True
        except:
            return False

    def Delete(self, id):
        """
        单个删除组织机构
        Args:
            id (string): 组织机构主键
        Returns:
            returnValue (True or False): 删除结果
        """
        try:
            #已删除组织机构Piorganize表中的DELETEMARK设置为1
            try:
                organize = Piorganize.objects.get(id=id)
            except Piorganize.DoesNotExist as e:
                return False
            organize.deletemark = 1
            organize.save()
            return True
        except Exception as e:
            return False

    def GetChildrensById(self, organizeId):
        """
        根据组织机构主键获取其指定分类下的子节点列表
        Args:
            organizeId (string): 组织机构主键
        Returns:
            returnValue (List): 子节点列表
        """
        try:
            returnValue = []
            returnValue.append(organizeId)
            for piorganize in Piorganize.objects.filter(Q(parentid=organizeId) & Q(deletemark=0)):
                returnValue.append(piorganize.id)
            return returnValue
        except Piorganize.DoesNotExist:
            return returnValue

    def GetDT(self):
        """
        获取组织机构列表
        Args:
        Returns:
            returnValue (List): 组织机构列表
        """
        returnValue = []
        try:
            # for organize in Piorganize.objects.all():
            #     returnValue.append(organize)
            # return returnValue

            returnValue = Piorganize.objects.filter(deletemark=0).order_by('sortcode')
            return returnValue
        except DatabaseError as e:
            return returnValue
        except TransactionManagementError as e:
            return returnValue

    def GetDTByIds(self, ids):
        """
        按主键获取组织机构列表
        Args:
            ids (List[string]): 主键数组
        Returns:
            returnValue (List): 组织机构列表
        """
        returnValue = []
        for id in ids:
            try:
                organize = Piorganize.objects.get(id=id)
                returnValue.append(organize)
            except Piorganize.DoesNotExist:
                continue
        return returnValue

    def GetDTByParent(self, parentId):
        """
        按父节点获取列表
        Args:
            parentId (string): 父节点主键
        Returns:
            returnValue (List): 组织机构列表
        """
        returnValue = []
        try:
            returnValue = Piorganize.objects.filter(parentid=parentId)
        except Exception as e:
            print(e)
        return returnValue

    def GetDTByValues(self, valueDic):
        """
        按键值对获取列表
        valueDic = {key:value, key:value, ...}
        Args:
            valueDic (Dic{key:value}): 参数和值对
        Returns:
            returnValue (Pioranize[]): 组织机构列表
        """
        q = Q()
        for i in valueDic:
            q.add(Q(**{i: valueDic[i]}), Q.AND)
        returnValue = Piorganize.objects.filter(q)
        return returnValue

    def GetEntity(self, id):
        """
        获取组织机构实体
        Args:
            id (string): 组织机构主键
        Returns:
            returnValue (Piuser or None): 组织机构实体
        """
        try:
            organize = Piorganize.objects.get(id=id)
            return organize
        except Piorganize.DoesNotExist:
            return None

    def GetList(self):
        """
        获取组织机构列表
        Args:
        Returns:
            returnValue (List): 组织机构列表
        """
        returnValue = []
        try:
            for organize in Piorganize.objects.all():
                returnValue.append(organize)
            return returnValue
        except DatabaseError as e:
            return returnValue
        except TransactionManagementError as e:
            return returnValue

    def GetListByParent(self, parentId):
        """
        按父节点获取列表
        Args:
            parentId (string): 父节点主键
        Returns:
            returnValue (List): 组织机构列表
        """
        returnValue = []
        try:
            returnValue = Piorganize.objects.filter(parentid=parentId)
        except Exception as e:
            print(e)
        return returnValue

    def MoveTo(self, organizeId, parentId):
        """
        移动组织机构
        Args:
            organizeId (string): 组织结构主键
            parentId (string): 更改后的父节点主键
        Returns:
            returnValue (True or False): 保存结果
        """
        try:
            organize = Piorganize.objects.get(id=organizeId)
            organize.parentid = parentId
            organize.save()
            return True
        except Piorganize.DoesNotExist:
            return False

    def SetDeleted(self, ids):
        """
        批量打删除标志
        Args:
            ids (string[]): 用户主键列表
        Returns:
            returnValue (True or False): 删除结果
        """
        try:
            organizes = Piorganize.objects.filter(id__in=ids)
            if len(organizes) == 0:
                return False
            for organize in organizes:
                #逻辑删除组织机构
                id = organize.id
                organize.deletemark = 1
                organize.save()
                #同步处理用户表组织机构相关数据
                Piuser.objects.filter(companyid=id).update(companyid = None, companyname=None)
                Piuser.objects.filter(subcompanyid=id).update(subcompanyid = None, subcompanyname = None)
                Piuser.objects.filter(departmentid=id).update(departmentid = None, departmentname = None)
                Piuser.objects.filter(subdepartmentid=id).update(subdepartmentid = None, subdepartmentname = None)
                Piuser.objects.filter(workgroupid=id).update(workgroupid = None, workgroupname = None)
                #同步处理员工表组织机构相关数据
                Pistafforganize.objects.filter(organizeid=id).update(deletemark=1)
                return True
        except Exception as e:
            return False

    def Update(self, entity):
        """
        更新组织机构
        Args:
            userEntity (Piorganize): 用户实体
        Returns:
            returnValue (string): 状态码
            returnMessage (string): 状态信息
        """
        try:
            entity.save()
            returnCode = StatusCode.statusCodeDic['OKUpdate']
            returnMessage = FrameworkMessage.MSG0010
            return returnCode,returnMessage
        except Exception as e:
            print(e)
            returnCode = StatusCode.statusCodeDic['Error']
            returnMessage = FrameworkMessage.MSG0001
            return returnCode, returnMessage

    def GetChildrensIdByCode(self, code):
        """
        根据编号获取子节点列表
        Args:
            code (string): 编号
        Returns:
            returnValue (List): 子节点列表
        """
        returnValue = []
        sqlQuery = "select id from piorganize where (LEFT(CODE,LENGTH('" + code + "'))='" + code + "')"
        childrens = DbCommonLibaray.executeQuery(self, sqlQuery)
        for c in childrens:
            returnValue.append(c.get('id'))
        return returnValue

    def GetInnerOrganizeDT(self):
        """
        获取内部组织机构
        Args:
        Returns:
            returnValue (Piorganize[]): 模块实体列表
        """
        getOnLine = False
        if OrganizeService.LastCheckOrgTime == datetime.datetime.min:
            getOnLine = True
        else:
            timeSpan = datetime.datetime.now() - OrganizeService.LastCheckOrgTime
            if timeSpan.minute * 60 + timeSpan.second >= SystemInfo.OnLineCheck * 100:
                getOnLine = True
        if OrganizeService.OnLineStateDT == None or getOnLine:
            OrganizeService.InnerOrganizeDT = Piorganize.objects.filter(Q(isinnerorganize=1) & Q(enabled=1)).order_by('sortcode')
            OrganizeService.LastCheckOrgTime = datetime.datetime.now()
        return OrganizeService.InnerOrganizeDT