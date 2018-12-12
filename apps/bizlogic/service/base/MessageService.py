# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2018/12/11 15:54'

def GetInnerOrganizeDT():
    pass

def GetUserDTByOrganize(organizeId):
    pass

def GetUserDTByRole(roleId):
    pass

def Send(receiverId, contents):
    pass

def SendGroupMessage(organizeId, roleId, contents):
    pass

def Remind(receiverId, contents):
    pass

def BatchSend(receiverIds, organizeIds, roleIds, messageEntity):
    pass

def Broadcast(message):
    pass

def MessageChek(onLineState, lastChekDate):
    pass

def GetDTNew(openId):
    pass

def ReadFromReceiver(reveiverId):
    pass

def Read(id):
    pass

def CheckOnLine(onLineState):
    pass

def GetOnLineState():
    pass

def GetUserSentMessagesByPage(userId, whereConditional, recordCount, pageIndex=0, pageSize=20, order=None):
    pass

def GetUserReceivedMessagesByPage(userId, whereConditional, recordCount, pageIndex=0, pageSize=20, order=None):
    pass

def GetMessagesByConditional(whereConditional, recordCount, pageIndex=0, pageSize=20, order=None):
    pass

def SetDeleted(ids):
    pass

def GetEntity(id):
    pass