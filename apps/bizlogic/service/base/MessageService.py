# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2018/12/11 15:54'

class MessageService(object):

    def GetInnerOrganizeDT(self):
        pass

    def GetUserDTByOrganize(self, organizeId):
        pass

    def GetUserDTByRole(self, roleId):
        pass

    def Send(self, receiverId, contents):
        pass

    def SendGroupMessage(self, organizeId, roleId, contents):
        pass

    def Remind(self, receiverId, contents):
        pass

    def BatchSend(self, receiverIds, organizeIds, roleIds, messageEntity):
        pass

    def Broadcast(self, message):
        pass

    def MessageChek(self, onLineState, lastChekDate):
        pass

    def GetDTNew(self, openId):
        pass

    def ReadFromReceiver(self, reveiverId):
        pass

    def Read(self, id):
        pass

    def CheckOnLine(self, onLineState):
        pass

    def GetOnLineState(self):
        pass

    def GetUserSentMessagesByPage(self, userId, whereConditional, recordCount, pageIndex=0, pageSize=20, order=None):
        pass

    def GetUserReceivedMessagesByPage(self, userId, whereConditional, recordCount, pageIndex=0, pageSize=20, order=None):
        pass

    def GetMessagesByConditional(self, whereConditional, recordCount, pageIndex=0, pageSize=20, order=None):
        pass

    def SetDeleted(self, ids):
        pass

    def GetEntity(self, id):
        pass