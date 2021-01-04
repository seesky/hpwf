# _*_ coding: utf-8 _*_
__author__ = 'baxuelong@163.com'
__date__ = '2018/12/11 16:56'

from apps.bizlogic.models import Cifile
from django.db.models import Q
from apps.utilities.message.StatusCode import StatusCode
from apps.utilities.message.FrameworkMessage import FrameworkMessage
from django.db.utils import DatabaseError
from django.db.transaction import TransactionManagementError
from apps.utilities.publiclibrary.DbCommonLibaray import DbCommonLibaray
import uuid,datetime

class FileService(object):

    def UpdateReadCount(self, id):
        """
        阅读次数要加一
        Args:
            id (string): 主键
        Returns:
            returnValue (True or False): 成功失败
        """
        try:
            file = Cifile.objects.get(id=id)
            file.readcount = file.readcount + 1
            file.save()
            return True
        except Cifile.DoesNotExist as e:
            return False

    def GetEntity(self, id):
        """
        获取实体
        Args:
            id (string): 主键
        Returns:
            returnValue (Cifile[]): 文件列表
        """
        try:
            user = Cifile.objects.get(id=id)
            return user
        except Cifile.DoesNotExist:
            return None

    def Exists(self, folderId, fileName):
        """
        判断是否存在
        Args:
            folderId (string): 目录id
            fileName (string): 文件名
        Returns:
            returnValue (True or False): 是否存在
        """
        try:
            Cifile.objects.get(Q(folderid=folderId) & Q(filename=fileName))
            return False
        except Cifile.DoesNotExist as e:
            return True

    def Download(self, id):
        FileService.UpdateReadCount(self, id)
        fileCountent = None
        pass

    def Upload(self, folderId, fileName, file, enabled):
        returnValue = FileService.GetId(self, folderId, fileName)
        if returnValue:
            #更新数据
            FileService.UpdateFile(returnValue, fileName, file)
        else:
            entity = Cifile()
            entity.folderid = folderId
            entity.filename = fileName
            entity.filecontent = file
            if enabled:
                entity.enabled = 1
            else:
                entity.enabled = 0
            returnValue = FileService.AddEntity(entity)
        returnValue

    def GetDTByFolder(self, folderId):
        """
        根据目录获取文件
        Args:
            folderId (string): 目录id
        Returns:
            returnValue (Cifile or None): 是否存在
        """
        sqlQuery = " SELECT " + 'ID'
        + "        ," + 'FOLDERID'
        + "        ," + 'FILENAME'
        + "        ," + 'FILEPATH'
        + "        ," + 'FILESIZE'
        + "        ," + 'READCOUNT'
        + "        ," + 'CATEGORY'
        + "        ," + 'DESCRIPTION'
        + "        ," + 'ENABLED'
        + "        ," + 'SORTCODE'
        + "        ," + 'CREATEUSERID'
        + "        ," + 'CREATEBY'
        + "        ," + 'CREATEON'
        + "        ," + 'MODIFIEDUSERID'
        + "        ," + 'MODIFIEDBY'
        + "        ," + 'MODIFIEDON'
        + "       , (SELECT " + 'FOLDERNAME'
        + " FROM " + 'cifolder'
        + " WHERE " + 'ID' + " = '" + 'FOLDERID' + "') AS folderfullname "
        + " FROM " + 'cifile'
        + " WHERE " + 'FOLDERID' + " = " + folderId;
        returnValue = DbCommonLibaray.executeQuery(self, sqlQuery)
        return returnValue

    def GetFileDTByPage(self, pageIndex=1, pageSize=20, whereConditional="", order=""):
        """
        分页获取文件
        Args:
            pageIndex (string): 页数
            pageSize (string): 每页数据大小
            whereConditional (string): 查询条件
            order (string): 排序方式
        Returns:
            returnValue (List[Cifile] or None): 文件列表
        """
        SelectField = 'ID'
        + "        ," + 'FOLDERID'
        + "        ," + 'FILENAME'
        + "        ," + 'FILEPATH'
        + "        ," + 'FILESIZE'
        + "        ," + 'READCOUNT'
        + "        ," + 'CATEGORY'
        + "        ," + 'DESCRIPTION'
        + "        ," + 'ENABLED'
        + "        ," + 'SORTCODE'
        + "        ," + 'CREATEUSERID'
        + "        ," + 'CREATEBY'
        + "        ," + 'CREATEON'
        + "        ," + 'MODIFIEDUSERID'
        + "        ," + 'MODIFIEDBY'
        + "        ," + 'MODIFIEDON'
        + "       , (SELECT " + 'FOLDERNAME'
        + " FROM " + 'cifolder'
        + " WHERE " + 'ID' + " = '" + 'FOLDERID' + "') AS FolderFullName ";

        returnValue = DbCommonLibaray.GetDTByPage('cifile', whereConditional, order, SelectField, pageIndex, pageSize)
        return len(returnValue),returnValue

    def DeleteByFolder(self, folderId):
        """
        分页获取文件
        Args:
            folderId (string): 目录id
        Returns:
            returnValue (int): 影响行数
        """
        returnValue = Cifile.objects.filter(Q(folderid=folderId)).delete()
        return returnValue

    def Add(userInfo, folderId, fileName, file, description, catefory, enabled):
        """
        添加文件
        Args:
            folderId (string): 目录id
            fileName (stirng): 文件名
            file (byte[]): 文件内容
            description (string): 文件描述
            category (string): 文件分类
            enabled (int): 是否有效
        Returns:
            returnValue (string): 文件主键
        """
        if FileService.Exists(None, folderId, fileName):
            return StatusCode.statusCodeDic.get('ErrorNameExist'),None
        else:
            fileEntity = Cifile()
            fileEntity.id = uuid.uuid4()
            fileEntity.folderid = folderId
            fileEntity.filename = fileName
            fileEntity.filecontent = file
            fileEntity.description = description
            fileEntity.category = catefory
            fileEntity.deletemark = 0
            fileEntity.createon = datetime.datetime.now()
            fileEntity.modifiedon = fileEntity.createon
            if enabled:
                fileEntity.enabled = 1
            else:
                fileEntity.enabled = 0
            FileService.AddEntity(None, fileEntity)
            return StatusCode.statusCodeDic.get('OKAdd'),fileEntity


    def Update(userInfo, id, folderId, fileName, description, enabled):
        """
        更新文件
        Args:
            id (string): 文件id
            folderId (string): 目录id
            fileName (stirng): 文件名
            description (string): 文件描述
            enabled (int): 是否有效
        Returns:
            returnValue (True or False): 更新是否成功
        """
        returnValue = 0
        try:
            returnValue = Cifile.objects.filter(id = id).update(folderid = folderId, filename = fileName, enabled = enabled, description = description, modifieduserid = userInfo.Id, modifiedby = userInfo.UserName, modifiedon = datetime.datetime.now())
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

    def UpdateFile(self, id, fileName, file):
        """
        更新文件
        Args:
            id (string): 文件id
            fileName (stirng): 文件名
            file (byte[]): 文件内容
        Returns:
            returnCode (string): 状态码
            returnMessage (string): 状态信息
        """
        returnValue = 0
        try:
            returnValue = Cifile.objects.filter(id = id).update(filename = fileName, filecontent = file)
            if returnValue > 0:
                returnCode = StatusCode.statusCodeDic['OKUpdate']
                returnMessage = FrameworkMessage.MSG0010
                return returnCode,returnMessage, returnValue
            else:
                returnCode = StatusCode.statusCodeDic['Error']
                returnMessage = FrameworkMessage.MSG0001
                return returnCode, returnMessage, returnValue
        except:
            returnCode = StatusCode.statusCodeDic['Error']
            returnMessage = FrameworkMessage.MSG0001
            return returnCode, returnMessage, returnValue

    def Rename(self, id, newName, enabled):
        """
        文件重命名
        Args:
            id (string): 文件id
            newName (stirng): 新文件名
            enabled (int): 是否有效
        Returns:
        """
        returnValue = 0
        try:
            returnValue = Cifile.objects.filter(id=id).update(filename=newName, enabled=enabled)
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

    def MoveTo(self, id, folderId):
        """
        移动文件
        Args:
            id (string): 文件id
            folderId (stirng): 目录id
        Returns:
            returnValue (True or False)
        """
        returnValue = 0
        try:
            returnValue = Cifile.objects.filter(id=id).update(folder=folderId)
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


    def BatchMoveTo(self, ids, folderId):
        """
        移动文件
        Args:
            ids (List[string]): 文件id列表
            folderId (stirng): 目录id
        Returns:
            returnValue (True or False)
        """
        returnValue = 0
        try:
            for id in ids:
                returnValue = returnValue + Cifile.objects.filter(id=id).update(folder=folderId)
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

        pass

    def Delete(self, id):
        """
        删除文件
        Args:
            id (string): 文件id
        Returns:
            returnValue (int)
        """
        returnValue = 0
        try:
            returnValue,v = Cifile.objects.filter(id = id).delete()
            return returnValue
        except Exception as e:
            return returnValue

    def BatchDelete(self, ids):
        """
        批量删除文件
        Args:
            ids (List[string]): 文件id列表
        Returns:
            returnValue (int)
        """
        returnValue = 0
        try:
            returnValue,v = Cifile.objects.filter(id__in=ids).delete()
            return returnValue
        except Exception as e:
            return returnValue

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

    def GetId(self, folderId, fileName):
        """
        获得主键
        Args:
            folderId (string): 目录ID
            fileName (string): 文件名
        Returns:
            returnValue (string or None): 文件主键
        """
        try:
            id = Cifile.objects.get(Q(folderid=folderId) & Q(filename=fileName)).id
            return id
        except Cifile.DoesNotExist as e:
            return None

    def AddEntity(self, fileEntity):
        """
        添加用户
        Args:
            userEntity (Piuser): 用户实体
        Returns:
            returnValue: 用户主键
        """
        try:
            fileEntity.save()
            returnCode = StatusCode.statusCodeDic['OKAdd']
            returnMessage = FrameworkMessage.MSG0009
            returnValue = fileEntity.id
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