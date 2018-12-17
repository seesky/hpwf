# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2018/12/11 14:25'

from django.db.utils import DatabaseError
from django.db.transaction import TransactionManagementError

from apps.bizlogic.models import Piorganize
from apps.bizlogic.models import Piuser
from apps.bizlogic.models import Pistaff

from apps.utilities.message.StatusCode import StatusCode
from apps.utilities.message.FrameworkMessage import FrameworkMessage
from apps.utilities.publiclibrary.DbCommonLibaray import DbCommonLibaray

class OrganizeService(object):
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
            for piorganize in Piorganize.objects.filter(parentid=organizeId):
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
            for organize in Piorganize.objects.all():
                returnValue.append(organize)
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

    def GetDTByValues(self, names, values):
        """
        按父节点获取列表
        Args:
            parentId (string): 父节点主键
        Returns:
            returnValue (List[Dic{}]): 组织机构列表
        """
        sqlQuery = 'select * from piorganize where '
        for name,value in names,values:
            sqlQuery = sqlQuery + names + '=' + value + ' AND '
        sqlQuery.rstrip(' AND ')
        returnValue = DbCommonLibaray.executeQuery(self, sqlQuery)
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
                Pistaff.objects.filter(organizeid=id).update(deletemark=1)
                return True
        except Exception as e:
            return False

    def Update(self, entity, statusMessage):
        """
        更新用户
        Args:
            userEntity (Piuser): 用户实体
        Returns:
            returnValue (string): 状态码
            returnMessage (string): 状态信息
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