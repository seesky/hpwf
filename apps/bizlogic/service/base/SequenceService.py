# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2018/12/11 16:22'

def Add(sequenceEntity, statusCode, statsMessage):
    pass

def Add(dataTable, statusCode, statusMessage):
    pass

def GetDT():
    pass

def GetDTByPage(recordCount, pageIndex=1, pageSize=20, whereConditional="", order=""):
    pass

def GetEntity(id):
    pass

def Update(entity, statusCode, statusMessage):
    pass

def Update(dataTable, statsCode, statsMessage):
    pass

def GetSequence(fullName):
    pass

def GetOldSequence(fullName, defaultSequence, sequenceLength, fillZeroPrefix):
    pass

def GetNewSequence(fullName, defaultSequence, sequenceLength, fillZeroPrefix):
    pass

def GetBatchSequence(fullName, count):
    pass

def GetReduction(fullName):
    pass

def Reset(ids):
    pass

def Delete(id):
    pass

def SetDeleted(id):
    pass

def BatchDelete(ids):
    pass