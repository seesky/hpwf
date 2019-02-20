# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2018/12/11 16:05'

from apps.bizlogic.models import Cifolder
from django.db.models import Q
import uuid,datetime
from apps.utilities.message.StatusCode import StatusCode
from apps.utilities.message.FrameworkMessage import FrameworkMessage
from django.db.utils import DatabaseError
from django.db.transaction import TransactionManagementError

class FolderService(object):

    def Exists(self, parentId, folderName):
        """
        判断是否存在
        Args:
            parentId (string): 父目录id
            folderName (string): 目录名
        Returns:
            returnValue (True or False): 是否存在
        """
        try:
            Cifolder.objects.get(Q(parentId=parentId) & Q(folderName=folderName))
            return False
        except Cifolder.DoesNotExist as e:
            return True

    def GetEntity(self, id):
        """
        获取实体
        Args:
            id (string): 主键
        Returns:
            returnValue (Cifolder[]): 文件列表
        """
        try:
            folder = Cifolder.objects.get(id=id)
            return folder
        except Cifolder.DoesNotExist:
            return None

    def GetDT(self, valueDic):
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
        returnValue = Cifolder.objects.filter(q)
        return returnValue

    def GetDTByParent(self, id):
        """
        按父节点获取列表
        Args:
            parentId (stirng): 父节点主键
        Returns:
            returnValue (Cifolder[]):
        """
        returnValue = Cifolder.objects.filter(Q(deletemark=0) & Q(parentid=id)).order_by('sortcode')
        return returnValue

    def AddByFolderName(userInfo, parentId, folderName, enabled):
        """
        添加
        Args:
            parentId (stirng): 父节点主键
            folderName (string):文件名
            enabled (int): 是否有效
        Returns:
            returnValue (string): 主键
        """
        if FolderService.Exists(None, parentId, folderName):
            return StatusCode.statusCodeDic.get('ErrorNameExist'), None
        else:
            folderEntity = Cifolder()
            folderEntity.id = uuid.uuid4()
            folderEntity.parentid = parentId
            folderEntity.foldername = folderName
            if enabled:
                folderEntity.enabled = 1
            else:
                folderEntity.enabled = 0
            folderEntity.deletemark = 0
            folderEntity.createon = datetime.datetime.now()
            folderEntity.createby = userInfo.UserName
            folderEntity.createuserid = userInfo.Id
            folderEntity.modifiedon = folderEntity.createon
            folderEntity.modifiedby = folderEntity.createby
            folderEntity.modifieduserid = userInfo.Id
            FolderService.Add(None, folderEntity)
            return StatusCode.statusCodeDic.get('OKAdd'), folderEntity.id


    def Add(self, folderEntity):
        """
        添加用户
        Args:
            userEntity (Piuser): 用户实体
        Returns:
            returnValue: 用户主键
        """
        try:
            folderEntity.save()
            returnCode = StatusCode.statusCodeDic['OKAdd']
            returnMessage = FrameworkMessage.MSG0009
            returnValue = folderEntity.id
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

    def Update(self, folderEntity):
        """
        更新文件夹
        Args:
            folderEntity (Cifolder): 目录实体
        Returns:
            returnValue (string): 状态码
            returnMessage (string): 状态信息
        """
        try:
            folderEntity.save()
            returnCode = StatusCode.statusCodeDic['OKUpdate']
            returnMessage = FrameworkMessage.MSG0010
            return returnCode,returnMessage
        except:
            returnCode = StatusCode.statusCodeDic['Error']
            returnMessage = FrameworkMessage.MSG0001
            return returnCode, returnMessage

    def GetDT(self):
        """
        获取文件列表
        Args:
        Returns:
            returnValue (List[Cifoler]): 文件夹列表
        """
        returnValue = Cifolder.objects.all()
        return returnValue

    def Rename(self, id, newName, enabled):
        """
        文件夹重命名
        Args:
            id (string): 文件id
            newName (stirng): 新文件夹名
            enabled (int): 是否有效
        Returns:
        """
        returnValue = 0
        try:
            returnValue = Cifolder.objects.filter(id=id).update(foldername=newName, enabled=enabled)
            if returnValue > 0:
                returnCode = StatusCode.statusCodeDic['OKUpdate']
                returnMessage = FrameworkMessage.MSG0010
                return returnCode, returnMessage, returnValue
            else:
                returnCode = StatusCode.statusCodeDic['Error']
                returnMessage = FrameworkMessage.MSG0001
                return returnCode, returnMessage, returnValue
        except:
            returnCode = StatusCode.statusCodeDic['Error']
            returnMessage = FrameworkMessage.MSG0001
            return returnCode, returnMessage, returnValue

    def Search(self, searchValue):
        pass

    def Delete(self, id):
        """
        删除文件夹
        Args:
            id (string): 文件夹id
        Returns:
            returnValue (int)
        """
        returnValue = 0
        try:
            returnValue, v = Cifolder.objects.filter(id=id).delete()
            return returnValue
        except Exception as e:
            return returnValue

    def BatchDelete(self, ids):
        returnValue = 0
        try:
            returnValue, v = Cifolder.objects.filter(id__in=ids).delete()
            return returnValue
        except Exception as e:
            return returnValue

    def MoveTo(self, folderId, parentId):
        """
        移动文件夹
        Args:
            folderId (string): 目录id
            parentId (stirng): 父目录id
        Returns:
            returnValue (True or False)
        """
        returnValue = 0
        try:
            returnValue = Cifolder.objects.filter(id=folderId).update(parentId=parentId)
            if returnValue > 0:
                returnCode = StatusCode.statusCodeDic['OKUpdate']
                returnMessage = FrameworkMessage.MSG0010
                return returnCode, returnMessage, returnValue
            else:
                returnCode = StatusCode.statusCodeDic['Error']
                returnMessage = FrameworkMessage.MSG0001
                return returnCode, returnMessage, returnValue
        except:
            returnCode = StatusCode.statusCodeDic['Error']
            returnMessage = FrameworkMessage.MSG0001
            return returnCode, returnMessage, returnValue

    def BatchMoveTo(self, folderIds, parentId):
        """
                移动文件夹
                Args:
                    folderId (string): 目录id
                    parentId (stirng): 父目录id
                Returns:
                    returnValue (True or False)
                """
        returnValue = 0
        try:
            returnValue = Cifolder.objects.filter(id__in=folderIds).update(parentId=parentId)
            if returnValue > 0:
                returnCode = StatusCode.statusCodeDic['OKUpdate']
                returnMessage = FrameworkMessage.MSG0010
                return returnCode, returnMessage, returnValue
            else:
                returnCode = StatusCode.statusCodeDic['Error']
                returnMessage = FrameworkMessage.MSG0001
                return returnCode, returnMessage, returnValue
        except:
            returnCode = StatusCode.statusCodeDic['Error']
            returnMessage = FrameworkMessage.MSG0001
            return returnCode, returnMessage, returnValue

    def BatchSave(self, dataTable):
        """
        批量保存
        Args:
            ids (List[string]): 文件id列表
        Returns:
            returnValue (int)
        """
        returnValue = 0
        try:
            for user in dataTable:
                user.save()
                returnValue = returnValue + 1
            return returnValue
        except:
            return returnValue