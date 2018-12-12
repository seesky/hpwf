# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2018/12/11 16:56'

def GetEntity(id):
    pass

def Exists(folderId, fileName):
    pass

def Download(id):
    pass

def Upload(folderId, fileName, file, enabled):
    pass

def GetDTByFolder(folderId):
    pass

def GetFileDTByPage(recordCount, pageIndex=1, pageSize=20, whereConditional="", order=""):
    pass

def DeleteByFolder(folderId):
    pass

def Add(folderId, fileName, file, description, catefory, enabled, statusCode, statusMessage):
    pass

def Update(id, folderId, fileName, description, enabled, statusCode, statusMessage):
    pass

def UpdateFile(id, fileName, file, statusCode, statusMessage):
    pass

def Rename(id, newName, enabled, statusCode, statusMessage):
    pass

def Search(searchValue):
    pass

def MoveTo(id, folderId):
    pass

def BatchMoveTo(ids, folderId):
    pass

def Delete(id):
    pass

def BatchDelete(ids):
    pass

def BatchSave(dataTable):
    pass