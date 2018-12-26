# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2018/12/11 16:56'

from apps.bizlogic.models import Cifile
from django.db.models import Q

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
        pass

    def GetDTByFolder(self, folderId):
        pass

    def GetFileDTByPage(self, recordCount, pageIndex=1, pageSize=20, whereConditional="", order=""):
        pass

    def DeleteByFolder(self, folderId):
        pass

    def Add(self, folderId, fileName, file, description, catefory, enabled, statusCode, statusMessage):
        pass

    def Update(self, id, folderId, fileName, description, enabled, statusCode, statusMessage):
        pass

    def UpdateFile(self, id, fileName, file, statusCode, statusMessage):
        pass

    def Rename(self, id, newName, enabled, statusCode, statusMessage):
        pass

    def Search(self, searchValue):
        pass

    def MoveTo(self, id, folderId):
        pass

    def BatchMoveTo(self, ids, folderId):
        pass

    def Delete(self, id):
        pass

    def BatchDelete(self, ids):
        pass

    def BatchSave(self, dataTable):
        pass