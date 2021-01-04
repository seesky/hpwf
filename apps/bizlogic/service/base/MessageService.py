# _*_ coding: utf-8 _*_
__author__ = 'baxuelong@163.com'
__date__ = '2018/12/11 15:54'

import datetime
from apps.utilities.publiclibrary.SystemInfo import SystemInfo
from apps.bizlogic.models import Piorganize
from django.db.models import Q
from apps.bizlogic.service.base.SequenceService import SequenceService
from apps.bizlogic.service.base.UserService import UserSerivce
from apps.bizlogic.models import Cimessage
from apps.bizlogic.models import Piuser
from apps.bizlogic.service.base.LogOnService import LogOnService
from apps.utilities.message.MessageCategory import MessageCategory
from apps.utilities.message.MessageFunction import MessageFunction
from apps.utilities.message.MessageStateCode import MessageStateCode
from apps.hadmin.MvcAppUtilties.CommonUtils import CommonUtils
import time,uuid
from apps.utilities.publiclibrary.DbCommonLibaray import DbCommonLibaray
from django.core.paginator import Paginator
from apps.bizlogic.service.base.LogService import LogService
from apps.utilities.message.FrameworkMessage import FrameworkMessage
import sys

class MessageService(object):

    Identity = False
    ReturnId = False
    LastCheckOnLineState = datetime.datetime.min
    OnLineStateDT = None

    def GetInnerOrganizeDT(self):
        #OrganizeService.GetInnerOrganizeDT(self)
        pass

    def GetUserDTByOrganize(self, organizeId):
        #UserService.GetDTByOrganizes(self, organizeIds)
        pass

    def GetUserDTByRole(self, roleId):
        #UserService.GetUserDTByRole()
        pass

    def Send(response, request, receiverId, contents, saveSend):
        """
        获取内部组织机构
        Args:
            receiverId (string): 接收者主键
            contents (string): 内容
        Returns:
            returnValue (string): 主键
        """
        returnValue = ''
        messageEntity = Cimessage()
        messageEntity.categorycode = MessageCategory.Send
        messageEntity.functioncode = MessageFunction.UserMessage
        messageEntity.receiverid = receiverId
        messageEntity.msgcontent = contents
        messageEntity.isnew = MessageStateCode.New
        messageEntity.readcount = 0
        messageEntity.deletemark = 0
        messageEntity.enabled = 1

        receiverIds = [messageEntity.receiverid]

        returnValue = MessageService.Sends(response, request, messageEntity, receiverIds)
        return returnValue

    def Sends(response, request, messageEntity, receiverIds, saveSend = True):
        """
        添加短信，可以发给多个人
        Args:
            messageEntity (string): 实体
            receiverIds (string): 接收者ID组
            saveSend (bool):
        Returns:
            returnValue (int): 影响行数
        """
        returnValue = 0
        #messageEntity.categorycode = MessageCategory.Receiver
        messageEntity.categorycode = 'Receiver'
        messageEntity.isnew = MessageStateCode.New
        messageEntity.ipaddress = CommonUtils.Current(response, request).IPAddress
        messageEntity.parentid = None
        messageEntity.deletemark = 0
        messageEntity.enabled = 1
        returnValue = returnValue + 1

        userEntity = Piuser()

        for id in receiverIds:
            messageEntity.parentid = None
            #messageEntity.categorycode = MessageCategory.Receiver
            messageEntity.categorycode = 'Receiver'
            messageEntity.receiverid = id
            #messageEntity.functioncode = MessageFunction.UserMessage
            messageEntity.functioncode = 'UserMessage'
            try:
                userEntity = Piuser.objects.get(id = id)
                messageEntity.receiverrealname = userEntity.realname
            except:
                pass
            messageEntity.enabled = 1
            messageEntity.isnew = 1

            if messageEntity.receiverid == CommonUtils.Current(response, request).Id:
                messageEntity.isnew = MessageStateCode.Old
            #接收信息
            parentId = MessageService.Add(messageEntity)

            if saveSend:
                messageEntity.id = uuid.uuid4()
                messageEntity.parentid = parentId
                #messageEntity.categorycode = MessageCategory.Send
                messageEntity.categorycode = 'Send'
                messageEntity.deletemark = 0
                messageEntity.enabled = 0
                MessageService.Add(messageEntity)
            returnValue = returnValue + 1
        return returnValue



    def SendGroupMessage(organizeId, roleId, contents):
        """
        发送组消息
        Args:
            organizeId (string): 组织机构主键
            roleId (string): 角色主键
            contents (string): 内容
        Returns:
        """
        returnValue = 0
        messageEntity = Cimessage()
        messageEntity.categorycode = MessageCategory.Send
        messageEntity.msgcontent = contents
        messageEntity.isnew = MessageStateCode
        messageEntity.readcount = 0
        messageEntity.deletemark = 0
        messageEntity.enabled = 1

        if organizeId:
            messageEntity.functioncode = MessageFunction.OrganizeMessage
            messageEntity.objectid = organizeId
        if roleId:
            messageEntity.functioncode = MessageFunction.RoleMessage
            messageEntity.objectid = roleId
        returnValue = MessageService.BatchSend('', organizeId, roleId)
        pass

    def Remind(self, receiverId, contents):
        pass

    def BatchSend(response, request, receiverId, organizeId, roleId, messageEntity, saveSend = True):
        """
        按时间获取列表
        Args:
            receiverId (string): 获取方主键
            organizeId (string): 组织机构主键
            roleId (string): 角色主键
            messageEntity (Cimessage): 消息实体
            saveSend (bool): 是否保存发送方信息
        Returns:
        """
        receiverIds = []
        organizeIds = []
        roleIds = []
        if receiverId:
            receiverIds = [receiverId]
        if roleId:
            roleIds = [roleId]
        if organizeId:
            organizeIds = [organizeId]
        return MessageService.BatchSends(response, request, receiverIds, organizeIds, roleIds, messageEntity)

    def BatchSends(response, request, receiverIds, organizeIds, roleIds, messageEntity):
        """
        按时间获取列表
        Args:
            receiverIds (string): 获取方主键
            organizeIds (string): 组织机构主键
            roleIds (string): 角色主键
            messageEntity (Cimessage): 消息实体
        Returns:
        """
        receiverIds = UserSerivce.GetUserIdsByOrganizeIdsAndRoleIds(None, receiverIds, organizeIds, roleIds)
        returnValue = MessageService.Sends(response, request, messageEntity, receiverIds)
        return returnValue

    def Broadcast(response, request, message):
        """
        广播消息
        Args:
            message (string): 内容
        Returns:
        """
        returnValue = 0
        receiverIds = list(Piuser.objects.filter(Q(enabled=1) & Q(deletemark=0)).values_list('id', flat=True))
        messageEntity = Cimessage()
        messageEntity.id = uuid.uuid4()
        #messageEntity.functioncode = MessageFunction.Remind
        messageEntity.functioncode = 'Remind'
        messageEntity.msgcontent = message
        messageEntity.isnew = 1
        messageEntity.readcount = 0
        messageEntity.enabled = 1
        messageEntity.deletemark = 0
        messageEntity.createon = datetime.datetime.now()
        messageEntity.modifiedon = messageEntity.createon
        returnValue = MessageService.BatchSends(response, request, receiverIds, '', '', messageEntity)
        return returnValue

    def GetNewCount(userInfo, messageFunction):
        returnValue = 0
        returnValue = (Cimessage.objects.filter(Q(isnew=int(MessageStateCode.New)) & Q(categorycode='Receiver') & Q(receiverid=userInfo.Id) & Q(deletemark=0) & Q(functioncode=messageFunction))).count()
        if returnValue:
            returnValue = int(returnValue)
        return returnValue

    def GetNewOne(userInfo):
        returnValue = Cimessage.objects.filter(Q(isnew=MessageStateCode.New) & Q(receiverid=userInfo.Id)).order_by('-')
        if returnValue.count() > 0:
            returnValue = returnValue[0]
        return returnValue

    def MessageChek(self, userInfo, onLineState, lastChekDate):
        """
        获取消息状态
        Args:
            userInfo (string): 用户
            onLineState (string): 用户在线状态
            lastChekDate (string): 最后检查日期
        Returns:
        """
        returnValue = []
        LogOnService.OnLine(None, userInfo.Id, onLineState)
        messageCount = MessageService.GetNewCount(userInfo, MessageFunction.Message)
        returnValue[0] = str(messageCount)
        if len(messageCount) > 0:
            messageEntity = MessageService.GetNewOne(userInfo)
            latCheckDate = datetime.datetime.min
            if messageEntity.createon:
                lastChekDate = messageEntity.createon
                returnValue[1] = time.struct_time(lastChekDate, SystemInfo.DateTimeFormat)
            returnValue[2] = messageEntity.createuserid
            returnValue[3] = messageEntity.createby
            returnValue[4] = messageEntity.objectid
            returnValue[5] = messageEntity.msgcontent
        return returnValue


    def GetDTNew(self, userInfo, openId):
        """
        获取消息状态
        Args:
            userInfo (string): 用户
            openId (string): 单点登录标识
        Returns:
        """
        myOpenId = userInfo.OpenId

        if not SystemInfo.CheckOnLine:
            try:
                myOpenId = Cimessage.objects.get(id=userInfo.Id).id
            except:
                myOpenId = ''
        if userInfo.OpenId == myOpenId:
            dataTable = Cimessage.objects.filter(Q(receiverid=userInfo.Id) & Q(categorycode="Receiver") & Q(isnew=MessageStateCode.New) & Q(deletemark=0) & Q(enabled=1)).order_by('createuserid','createon')[:20]
        openId = myOpenId
        return openId,dataTable

    def ReadFromReceiver(userInfo, reveiverId):
        """
        获取特定用户的新信息
        Args:
            userInfo (string): 用户
            reveiverId (string): 当前交互的用户
        Returns:
        """
        #读取发给我的信息
        dataTable = Cimessage.objects.filter(Q(isnew=MessageStateCode.New) & Q(receiverid=userInfo.Id) & Q(createuserid=reveiverId)).order_by('sortcode')
        dataTable.update(isnew=MessageStateCode.Old)
        return dataTable


    def Read(userInfo, id):
        """
        获取特定用户的新信息
        Args:
            userInfo (string): 用户
            id (string): 主键
        Returns:
        """
        returnValue = 0
        messageEntity = Cimessage.objects.get(id = id)
        #针对“已发送”的情况
        if messageEntity.receiverid == userInfo.Id:
            #针对“删除的信息”的情况
            if str(messageEntity.isnew) == MessageStateCode.New:
                messageEntity.isnew = MessageStateCode.Old
                messageEntity.readdate = datetime.datetime.now()
                messageEntity.readcount = messageEntity.readcount + 1
                messageEntity.save()
            else:
                messageEntity.readcount = messageEntity.readcount + 1
                messageEntity.save()

        returnValue = returnValue + 1
        return returnValue

    def CheckOnLine(userInfo, onLineState):
        """
        检查在线状态
        Args:
            userInfo (string): 用户
            onLineState (string): 用户在线状态
        Returns:
            returnValue (int): 离线人数
        """
        #设置为在线状态
        LogOnService.OnLine(None, userInfo.Id, onLineState)
        returnValue = LogOnService.CheckOnLine(None)
        return returnValue

    def GetOnLineState(userInfo):
        """
        获取在线用户列表
        Args:
            userInfo (string): 用户
        Returns:
            returnValue (Ciuser[]): 数据表
        """
        #设置为在线状态
        getOnLine = False
        LogOnService.OnLine(None, userInfo.Id)
        if MessageService.LastCheckOnLineState == datetime.datetime.min:
            getOnLine = True
        else:
            timeSpan = datetime.datetime.now() - MessageService.LastCheckOrgTime
            if timeSpan.minute * 60 + timeSpan.second >= SystemInfo.OnLineCheck * 100:
                getOnLine = True
        if MessageService.OnLineStateDT == None or getOnLine:
            #检查用户在线状态(服务器专用)
            LogOnService.CheckOnLine()
            MessageService.OnLineStateDT = LogOnService.GetOnLineStateDT(None)
            MessageService.LastCheckOnLineState = datetime.datetime.now()
        return MessageService.OnLineStateDT

    def GetUserSentMessagesByPage(userInfo, userId, whereConditional, pageIndex=0, pageSize=20, order=None):
        """
        得到指定用户已发送的消息
        Args:
            userInfo (string): 用户
            userId (string):  指定用户主键
            whereConditional (string): 条件表达式
            pageIndex (string): 当前页
            pageSize (string): 每页显示
            order  (string): 排序
        Returns:
            returnValue (Ciuser[]): 数据表
        """
        if not userId:
            userId = userInfo.Id

        if whereConditional:
            whereConditional = whereConditional + " AND "
        whereConditional = whereConditional + "deletemark = 0 and enabled = 1 and createuserid = '" + userId + "'"
        if not order:
            order = ' createon desc '
        if whereConditional:
            whereConditional = "WHERE " + whereConditional

        sqlQuery = "select id from cimessage " + whereConditional + " order by " + order
        messageDT = DbCommonLibaray.executeQuery(None, sqlQuery)
        pages = Paginator(messageDT, pageSize)
        recordCount = pages.count
        return recordCount,pages.page(pageIndex)


    def GetUserReceivedMessagesByPage(userInfo, userId, whereConditional, pageIndex=0, pageSize=20, order=None):
        """
        得到指定用户收到的消息
        Args:
            userInfo (string): 用户
            userId (string):  指定用户主键
            whereConditional (string): 条件表达式
            pageIndex (string): 当前页
            pageSize (string): 每页显示
            order  (string): 排序
        Returns:
            returnValue (Cimessage[]): 数据表
        """
        if not userId:
            userId = userInfo.Id
        if whereConditional:
            whereConditional = whereConditional + " AND "
        whereConditional = whereConditional + "deletemark = 0 and enabled = 1 and createuserid = '" + userId + "'"
        if not order:
            order = ' desc '
        sqlQuery = "select id from cimessage " + whereConditional + " order by " + order
        messageDT = DbCommonLibaray.executeQuery(None, sqlQuery)
        pages = Paginator(messageDT, pageSize)
        recordCount = pages.count
        return recordCount, pages.page(pageIndex)

    def GetMessagesByConditional(userInfo, whereConditional, pageIndex=0, pageSize=20, order=None):
        """
        通过指定条件得到消息
        Args:
            userInfo (string): 用户
            whereConditional (string): 条件表达式
            pageIndex (string): 当前页
            pageSize (string): 每页显示
            order  (string): 排序
        Returns:
            returnValue (Cimessage[]): 数据表
        """
        if not order:
            order = "createon DESC "
        if not userInfo.IsAdministrator:
            if whereConditional:
                whereConditional = whereConditional + " AND (" + 'receiverid' + "='" + userInfo.Id + "' OR " \
                                     + 'createuserid' + "='" + userInfo.Id + "')"
            else:
                whereConditional = whereConditional + 'receiverid' + "='" + userInfo.Id + "' OR " \
                                     + 'createuserid' + "='" +  userInfo.Id + "'"
        if whereConditional:
            whereConditional = whereConditional + " AND " + 'deletemark' + " = 0"
        else:
            whereConditional = whereConditional + ' deletemark = 0 '

        if whereConditional:
            sqlQuery = "select * from cimessage where " + whereConditional + " order by " + order
        else:
            sqlQuery = "select * from cimessage"+ " order by " + order

        dataTable = DbCommonLibaray.executeQuery(None, sqlQuery)
        pages = Paginator(dataTable, pageSize)
        recordCount = pages.count
        return recordCount, pages.page(pageIndex)


    def SetDeleted(userInfo, ids):
        """
        批量逻辑删除消息
        Args:
            userInfo (string): 用户
            ids (List[string]): 主键数组
        Returns:
            returnValue (Cimessage[]): 数据表
        """
        LogService.WriteLog(userInfo, __class__.__name__, FrameworkMessage.MessageService,
                            sys._getframe().f_code.co_name, FrameworkMessage.MessageService_SetDeleted, str(ids))
        returnValue = Cimessage.objects.filter(id__in=ids).update(deletemark=1)
        return returnValue

    def GetEntity(self, id):
        """
        取得实体
        Args:
            id (string): 主键
        Returns:
            returnValue (Cimessage[]): 数据表
        """
        try:
            returnValue = Cimessage.objects.get(id = id)
            return returnValue
        except Cimessage.DoesNotExist as e:
            returnValue = None
            return returnValue

    def Add(cIMESSAGEEntity):
        """
        添加实体
        Args:
            cIMESSAGEEntity (Cimessage): 实体
        Returns:
            returnValue (string): 主键
        """
        return MessageService.AddEntity(cIMESSAGEEntity)

    def AddEntity(cIMESSAGEEntity):
        """
        添加实体
        Args:
            cIMESSAGEEntity (Cimessage): 实体
        Returns:
            returnValue (string): 主键
        """
        sequence = ''
        if cIMESSAGEEntity.sortcode == None or cIMESSAGEEntity.sortcode == 0:
            sequence = SequenceService.GetSequence(None, 'CIMESSAGE')
            cIMESSAGEEntity.sortcode = int(sequence)
        cIMESSAGEEntity.save()
        return cIMESSAGEEntity.id