# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2018/12/11 15:01'

from apps.bizlogic.models import Piuser
from django.db.utils import DatabaseError
from django.db.transaction import TransactionManagementError
from utilities.message.StatusCode import StatusCode
from utilities.message.FrameworkMessage import FrameworkMessage

class UserSerivce(object):
    """
    用户服务
    """

    def __init__(self):
        object.__init__()

    def Exists(self, fieldNames, fieldValue):
        pass

    def AddUser(self, userEntity, statusCode, statusMessage):
        """
        添加用户
        Args:
            userEntity (Piuser): 用户实体
            statusCode (string): 状态码
            statusMessage (string): 状态信息
        Returns:
            returnValue: 用户主键
        """
        try:
            userEntity.save()
            returnCode = StatusCode.statusCodeDic['OKAdd']
            returnMessage = FrameworkMessage.MSG0009
            returnValue = returnCode
            return returnCode, returnMessage, returnValue
        except DatabaseError as e:
            print(e)
        except TransactionManagementError as e:
            print(e)

    def GetEntity(id):
        """
        获取用户实体
        Args:
            id (string): 用户主键
        Returns:
            Piuser: 用户实体
        """
        user = Piuser.objects.get(id=id)
        return user

    def GetEntityByUserName(self, userName):
        pass

    def GetDT(self):
        pass

    def GetDTByPage(self, searchValue, departmentId, roleId, recordCount, pageIndex=0, pageSize=50, order=None):
        pass

    def GetList(self):
        pass

    def GetDTByIds(self, ids):
        pass

    def GetListByIds(self, ids):
        pass

    def UpdateUser(self, userEntity, statusCode, statusMessage):
        pass

    def Search(self, searchValue, auditStatus, roleIds):
        pass

    def SetUserAuditStates(self, ids, auditStates):
        pass

    def Delete(self, id):
        pass

    def BatchDelete(self, ids):
        pass

    def SetDeleted(self, ids):
        pass

    def BatchSave(self, dataTable):
        pass

    def GetCompanyUser(self):
        pass

    def GetDepartmentUser(self):
        pass

    def GetDepartmentUser(self, departmentId, containChildren):
        pass

    def GetListByDepartment(self, departmentId, containChildren):
        pass