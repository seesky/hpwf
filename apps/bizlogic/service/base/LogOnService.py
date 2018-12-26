# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2018/12/11 17:04'

from apps.utilities.publiclibrary.UserInfo import UserInfo
from apps.utilities.publiclibrary.SystemInfo import SystemInfo
from apps.utilities.publiclibrary.DbCommonLibaray import DbCommonLibaray
from apps.utilities.message.AuditStatus import AuditStatus
from utilities.message.StatusCode import StatusCode
from apps.bizlogic.models import Piuserlogon
from apps.bizlogic.models import Piuser

from django.db.models import Q

class LogOnService(object):

    def LogOnByOpenId(self, openId):
        """
        按唯一识别码登录
        Args:
            openId (string): 唯一识别码
        Returns:
            returnValue(Piuser): 用户实体
        """
        returnUserInfo = None
        #先侦测是否在线
        LogOnService.CheckOnLine()

        ReturnStatusCode = StatusCode.statusCodeDic['UserNotFound']
        try:
            dt = Piuserlogon.objects.get(openid=openId)
            userEntity = Piuser.objects.get(id=dt.id)
            userLogOnEntity = Piuserlogon.objects.get(id=userEntity.id)
            #TODO:还需要添加登录动作
            return returnUserInfo
        except Piuserlogon.DoesNotExist as e:
            return returnUserInfo


    def LogOnByUserName(self, userName, returnStatusCode, returnStatusMessage):
        pass

    def UserLogOn(self, userName, password, openId, craeteOpenId, returnStatusCode, returnStatusMessage):
        pass

    def GetEntity(self, id):
        pass

    def Update(self, entity):
        pass

    def GetUserDT(self):
        pass

    def GetStaffUserDT(self):
        pass

    def AccountActivation(self, openId, statusCode, statusMessage):
        pass

    def OnLine(self, onLineState=1):
        pass

    def OnExit(self):
        pass

    def ServerCheckOnLine(self):
        pass

    def SetPassword(self, userIds, password, returnStatusCode, returnStatusMessage):
        pass

    def ChangePassword(self, oldPassword, newPassword, statusCode, statusMessage):
        pass

    def UserIsLogOn(self):
        pass

    def LockUser(self, userName):
        pass

    def UnLockUser(self, userName):
        pass

    def UserDimission(self, userName, dimissionCause, dimissionDate, dimissionWhither=None):
        pass

    def CheckOnLine(self):
        """
        检查用户在线状态(服务器专用)
        Args:
        Returns:
            returnValue(int): 影响行数
        """
        returnValue = 0
        # 是否更新访问日期信息
        if not SystemInfo.UpdateVisit:
            return returnValue

        sqlQuery = " UPDATE piuserlogon " \
        + "  SET useronline = 0 " \
        + "  WHERE (lastvisit IS NULL) " \
        + "  OR ((useronline > 0) AND (lastvisit IS NOT NULL) AND ( DATE_ADD ( LastVisit, Interval " + str(SystemInfo.OnLineTime0ut) + " SECOND) < now()))";

        returnValue = DbCommonLibaray.executeQuery(self, sqlQuery)
        return returnValue

    def LogOn(self, userName, password, openId=None, createNewOpenId=False, ipAddress=None, macAddress=None, checkUserPassword=True):
        ReturnStatusCode = ''
        userInfo = UserInfo()
        realName = ''
        if UserInfo:
            realName = userInfo.RealName
            if ipAddress:
                ipAddress = UserInfo.IPAddress
            if macAddress:
                macAddress = UserInfo.MACAddress

        #01: 系统是否采用了在线用户的限制
        if SystemInfo.OnLineLimit > 0 and self.CheckOnLineLimit():
            ReturnStatusCode = StatusCode.statusCodeDic['ErrorOnLineLimit']
            return userInfo

        #02. 默认为用户没有找到状态，查找用户
        #这是为了达到安全要求，不能提示用户未找到，那容易让别人猜测到帐户
        if SystemInfo.EnableCheckPasswordStrength:
            ReturnStatusCode = StatusCode.statusCodeDic['ErrorLogOn']
        else:
            ReturnStatusCode = StatusCode.statusCodeDic['UserNotFound']

        #03. 查询数据库中的用户数据？只查询未被删除的
        dataTable = Piuser.objects.filter(Q(deletemark=0) & Q(username=userName))
        if dataTable.count() == 0:
            #TODO:若没数据再工号、邮件、手机号等方式登录
            pass

        userEntity = None
        userLogOnEntity = None
        if dataTable.count() > 1:
            ReturnStatusCode = StatusCode.statusCodeDic['UserDuplicate']
        elif dataTable.count() == 1:
            #05. 判断密码，是否允许登录，是否离职是否正确
            userEntity = dataTable[0]
            if userEntity.AuditStatus and userEntity.AuditStatus.endswith(AuditStatus.WaitForAudit):
                ReturnStatusCode = AuditStatus.WaitForAudit
                return userInfo

            #用户无效、已离职的
            if userEntity.isdimission ==1 or userEntity.enabled ==0:
                ReturnStatusCode = StatusCode.statusCodeDic['LogOnDeny']
                return userInfo

            #用户是否有效的
            if userEntity.enabled == -1:
                ReturnStatusCode = StatusCode.statusCodeDic['UserNotActive']
                return userInfo

            userLogOnEntity = Piuserlogon.objects.get(id=userEntity.id)




    def CheckOnLineLimit(self):
        """
        检查用户在线状态(服务器专用)
        Args:
        Returns:
            returnValue(int): 影响行数
        """
        returnValue = False
        self.CheckOnLine()
        userOnLine = Piuserlogon.objects.filter(useronline__gt=0)
        if userOnLine and SystemInfo.OnLineLimit <= userOnLine.count():
            returnValue = True
        return returnValue