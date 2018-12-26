# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2018/12/11 16:05'

class FolderService(object):

    def GetEntity(self, id):
        pass

    def GetDT(self, name, value):
        pass

    def GetDTByParent(self, id):
        pass

    def AddByFolderName(self, parentId, folderName, enabled, statusCode, statusMessage):
        pass

    def Add(self, folderEntity, statusCode, statusMessage):
        pass

    def Update(self, folderEntity, statusCode, statusMessage):
        pass

    def GetDT(self):
        pass

    def Rename(self, id, newName, enabled, statusCode, statusMessage):
        pass

    def Search(self, searchValue):
        pass

    def Delete(self, id):
        pass

    def BatchDelete(self, ids):
        pass

    def MoveTo(self, folderId, parentId):
        pass

    def BatchMoveTo(self, folderIds, parentId):
        pass

    def BatchSave(self, dataTable):
        pass