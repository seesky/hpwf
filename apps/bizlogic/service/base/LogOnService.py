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
import time
import datetime
from apps.bizlogic.service.base.ParameterService import ParameterService
from apps.utilities.publiclibrary.CheckIPAddress import CheckIPAddress
from apps.utilities.publiclibrary.SecretHelper import SecretHelper
from apps.bizlogic.models import Pirole
from apps.bizlogic.service.permission.PermissionService import PermissionService
import uuid
from django.db.models import Q,F

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
            if userEntity.username or userEntity.username != 'Administrator':
                #06. 允许登录时间是否有限制
                if userLogOnEntity.AllowEndTime:
                    userLogOnEntity.AllowEndTime = time.struct_time(tm_year=datetime.datetime.now().year, tm_mon=datetime.datetime.now().month, tm_mday=datetime.datetime.now().day, tm_hour=userLogOnEntity.AllowEndTime.Value.Minute, tm_min=userLogOnEntity.AllowEndTime.Value.Minute, tm_sec=userLogOnEntity.AllowEndTime.Value.Second)
                if userLogOnEntity.AllowStartTime:
                    userLogOnEntity.AllowStartTime = time.struct_time(tm_year=datetime.datetime.now().year,
                                                                    tm_mon=datetime.datetime.now().month,
                                                                    tm_mday=datetime.datetime.now().day,
                                                                    tm_hour=userLogOnEntity.AllowStartTime.Value.Minute,
                                                                    tm_min=userLogOnEntity.AllowStartTime.Value.Minute,
                                                                    tm_sec=userLogOnEntity.AllowStartTime.Value.Second)
                    if datetime.datetime.now() < userLogOnEntity.AllowStartTime:
                        ReturnStatusCode = StatusCode.statusCodeDic['UserLocked']
                        return userInfo
                if userLogOnEntity.AllowEndTime:
                    if datetime.datetime.now() > userLogOnEntity.AllowEndTime:
                        ReturnStatusCode = StatusCode.statusCodeDic['UserLocked']
                        return userInfo

                #07. 锁定日期是否有限制
                if userLogOnEntity.LockStartDate and datetime.datetime.now() > userLogOnEntity.LockStartDate:
                    if userLogOnEntity.LockEndDate or datetime.datetime.now() < userLogOnEntity.LockEndDate:
                        ReturnStatusCode = StatusCode.statusCodeDic['UserLocked']
                        return userInfo
        #08. 是否检查用户IP地址，是否进行访问限制？管理员不检查IP. && !this.IsAdministrator(userEntity.Id.ToString()
        if SystemInfo.EnableCheckIPAddress and userLogOnEntity.CheckIPAddress == 1 and (userEntity.username != 'Administrator' or userEntity.code == 'Administrator'):
            if ipAddress:
                if ParameterService.Exists(self, userEntity.id, 'IPAddress'):
                    if not CheckIPAddress.CheckIPAddress(self, ipAddress, userEntity.id):
                        ReturnStatusCode = StatusCode.statusCodeDic['ErrorIPAddress']
                        return userInfo

            #没有设置MAC地址时不检查
            if macAddress:
                if ParameterService.Exists(self,userEntity.id, 'MacAddress'):
                    if not CheckIPAddress.CheckIPAddress(self, macAddress, userEntity.id):
                        ReturnStatusCode = StatusCode.statusCodeDic['ErrorMacAddress']
                        return userInfo

        #10. 只允许登录一次，需要检查是否自己重新登录了，或者自己扮演自己了
        if UserInfo and UserInfo.id != userEntity.id:
            if SystemInfo.CheckOnLine and userLogOnEntity.multiuserlogin == 0 and userLogOnEntity.useronline > 0:
                isSelf = False
                if openId:
                    if userLogOnEntity.openid:
                        if userLogOnEntity.openid == openId:
                            isSelf = True
                if not isSelf:
                    ReturnStatusCode = StatusCode.statusCodeDic['ErrorOnLine']
                    return userInfo

        #04. 系统是否采用了密码加密策略？
        if checkUserPassword and SystemInfo.EnableEncryptServerPassword:
            password = SecretHelper.AESEncrypt(self, password)

        #11. 密码是否正确(null 与空看成是相等的)
        if userLogOnEntity.userpassword and password:
            userPasswordOK = True
            #用户密码是空的
            if not userLogOnEntity.userpassword:
                #但是输入了不为空的密码
                if password:
                    userPasswordOK = False
            else:
                #用户的密码不为空，但是用户是输入了密码、 再判断用户的密码与输入的是否相同
                userPasswordOK = password and userLogOnEntity.userpassword == password

            #用户的密码不相等
            if not userPasswordOK:
                userLogOnEntity.passworderrorcount = userLogOnEntity.passworderrorcount + 1
                if SystemInfo.PasswordErrorLockLimit > 0 and userLogOnEntity.passworderrorcount >= SystemInfo.PasswordErrorLockLimit:
                    #密码错误锁定周期若为0，直接设帐号无效，需要管理员审核
                    if SystemInfo.PasswordErrorLockCycle == 0:
                        Piuser.objects.filter(id=userEntity.id).update( enabled=0,auditstatus=AuditStatus.WaitForAudit)
                    else:
                        userLogOnEntity.lockstartdate = datetime.datetime.now()
                        userLogOnEntity.lockenddate = datetime.datetime.now() + datetime.timedelta(minutes=SystemInfo.PasswordErrorLockCycle)
                        Piuserlogon.objects.filter(id=userEntity.id).update(lockstartdate=userLogOnEntity.lockstartdate, lockenddate=userLogOnEntity.lockenddate)
                else:
                    Piuserlogon.objects.filter(id=userEntity.id).update(passworderrorcount=userLogOnEntity.passworderrorcount)
                '''
                    密码错误后处理：
                    11.1：记录日志
                    LogManager.Instance.Add(DBProvider, userEntity.Id.ToString(), userEntity.RealName, "LogOn", RDIFrameworkMessage.UserManager, "LogOn", RDIFrameworkMessage.UserManager_LogOn, userEntity.RealName, ipAddress, RDIFrameworkMessage.MSG0088);
                    TODO: 11.2：看当天（24小时内）输入错误密码多少次了？
                    TODO: 11.3：若输错密码数量已经超过了系统限制，则用户被锁定系统设定的小时数。
                    TODO: 11.4：同时处理返回值，由于输入错误密码次数过多导致被锁定，登录时应读取这个状态比较，时间过期后应处理下状态。
                    密码强度检查，若是要有安全要求比较高的，返回的提醒消息要进行特殊处理，不能返回非常明确的提示信息。
                '''
                if SystemInfo.EnableCheckPasswordStrength:
                    ReturnStatusCode = StatusCode.statusCodeDic['ErrorLogOn']
                else:
                    ReturnStatusCode = StatusCode.statusCodeDic['PasswordError']
                return userInfo

        #12. 更新IP地址，更新MAC地址
        userLogOnEntity.passworderrorcount = 0
        if ipAddress:
            userLogOnEntity.ipaddress = ipAddress
        if macAddress:
            userLogOnEntity.macaddress = macAddress

        Piuserlogon.objects.filter(id=userEntity.id).update(passworderrorcount=0, ipaddress=ipAddress, macaddress=macAddress)
        #可以正常登录了
        ReturnStatusCode = StatusCode.statusCodeDic['OK']

        #13. 登录、重新登录、扮演时的在线状态进行更新
        #userLogOnManager.ChangeOnLine(userEntity.Id);

        userInfo = self.ConvertToUserInfo(self, userInfo, userEntity, userLogOnEntity)
        userInfo.IPAddress = ipAddress
        userInfo.MACAddress = macAddress
        userInfo.Password = password
        #这里是判断用户是否为系统管理员的
        userInfo.IsAdministrator = PermissionService.IsAdministrator(self, userEntity)
        '''
        // 数据找到了，就可以退出循环了
                /*
                // 获得员工的信息
                if (userEntity.IsStaff == 1)
                {
                    PiStaffManager staffManager = new PiStaffManager(DBProvider, UserInfo);
                    //这里需要按 员工的用户ID来进行查找对应的员工-用户关系
                    PiStaffEntity staffEntity = new PiStaffEntity(staffManager.GetDT(PiStaffTable.FieldUserId, userEntity.Id));
                    if (!string.IsNullOrEmpty(staffEntity.Id))
                    {
                        userInfo = staffManager.ConvertToUserInfo(staffEntity, userInfo);
                    }

                }*/
        '''

        #记录系统访问日志
        if ReturnStatusCode == StatusCode.statusCodeDic['OK']:
            if not userInfo.OpenId:
                createNewOpenId = True
            if createNewOpenId:
                userInfo.OpenId = self.UpdateVisitDate(self, userEntity.id, createNewOpenId)
            else:
                self.UpdateVisitDate(self, userEntity.id, createNewOpenId)
        return userInfo

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

    def ConvertToUserInfo(self, userInfo, userEntity, userLogOnEntity):
        """
        Args:
        Returns:
        """
        userInfo.Id = userEntity.id
        userInfo.Code = userEntity.code
        userInfo.UserName = userEntity.username
        userInfo.CompanyId = userEntity.companyid
        userInfo.CompanyName = userEntity.companyname
        userInfo.DepartmentId = userEntity.departmentid
        userInfo.DepartmentName = userEntity.departmentname
        userInfo.WorkgroupId = userEntity.workgroupid
        userInfo.WorkgroupName = userEntity.workgroupname

        if userLogOnEntity:
            userInfo.OpenId = userLogOnEntity.openid

        if not userEntity.securitylevel:
            userEntity.securitylevel = 0
        else:
            userInfo.SecurityLevel = int(userEntity.securitylevel)

        if userEntity.roleid:
            #获取角色名称
            try:
                role = Pirole.objects.get(id=userEntity.roleid)
                userInfo.RoleName = role.realname
                userInfo.RoleId = role.id
            except Pirole.DoesNotExist as e:
                pass
        return userInfo

    def UpdateVisitDate(self, userId, createOpenId = False):
        """
        更新访问当前访问状态
        Args:
            userId (string): 用户主键
            createOpenId (string): 是否每次都产生新的OpenId
        Returns:
            returnValue (string): OpenId
        """
        userLogOnEntity = Piuserlogon.objects.get(id=userId)

        result = ''
        sqlQuery = ''
        #是否更新访问日期信息
        if SystemInfo.UpdateVisit:
            #第一次登录时间
            if not userLogOnEntity.firstvisit:
                Piuserlogon.objects.filter(Q(id=userLogOnEntity.id) & Q(firstvisit__isnull=True)).update(useronline=1, firstvisit=datetime.datetime.now())
            else:
            #最后一次登录时间
                if createOpenId:
                    Piuserlogon.objects.filter(Q(id=userLogOnEntity.id)).update(previousvisit=F('lastvisit'), useronline=1, lastvisit=datetime.datetime.now(), logoncount=F('logoncount')+1)
        else:
            if createOpenId:
                result = uuid.uuid1()
                Piuserlogon.objects.filter(Q(id=userLogOnEntity.id)).update(passworderrorcount = 0, openid = result)
        return result