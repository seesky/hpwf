# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2018/12/11 16:22'

class SequenceService(object):
    FillZeroPrefix = True  # 是否前缀补零
    DefaultSequence = 1000  # 默认升序序列号
    DefaultReduction = 9999999  # 默认降序序列号
    DefaultPrefix = ""  # 默认的前缀
    DefaultSeparator = ""  # 默认分隔符
    DefaultStep = 1  # 递增或者递减数步调
    DefaultSequenceLength = 8  # 默认的排序码长度
    SequenceLength = 8  # 序列长度
    UsePrefix = True  # 是否采用前缀，补充0方式

    def Add(self, sequenceEntity, statusCode, statsMessage):
        pass

    def Add(self, dataTable, statusCode, statusMessage):
        pass

    def GetDT(self):
        pass

    def GetDTByPage(self, recordCount, pageIndex=1, pageSize=20, whereConditional="", order=""):
        pass

    def GetEntity(self, id):
        pass

    def Update(self, entity, statusCode, statusMessage):
        pass

    def GetSequence(self, fullName):
        pass

    def GetOldSequence(self, fullName, defaultSequence, sequenceLength, fillZeroPrefix):
        pass

    def GetNewSequence(self, fullName, defaultSequence, sequenceLength, fillZeroPrefix):
        pass

    def GetBatchSequence(self, fullName, count):
        returnValue = []
        pass

    def GetReduction(self, fullName):
        pass

    def Reset(self, ids):
        pass

    def Delete(self, id):
        pass

    def SetDeleted(self, id):
        pass

    def BatchDelete(self, ids):
        pass