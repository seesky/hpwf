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
from apps.utilities.publiclibrary.ValidateUtil import ValidateUtil

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

    def UserLogOn(userName, password, openId, createOpenId):
        """
        用户登录
        Args:
            userName (string): 用户名
            password (string): 密码
            openId (string): 单点登录标识
            createOpenId (string): 重新创建单点登录标识
        Returns:
            returnValue (UserInfo): 实体
        """
        returnStatusCode = StatusCode.statusCodeDic['DbError']
        returnCode = ''
        returnMessage = ''
        returnUserInfo = None
        returnStatusCode,returnUserInfo = LogOnService.LogOn(userName, password, openId, createOpenId)
        return returnStatusCode,returnUserInfo

    def GetEntity(self, id):
        """
        获取实体
        Args:
            id (string): 主键
        Returns:
            returnValue (Piuserlogon or None): 实体
        """
        try:
            return Piuserlogon.objects.get(id = id)
        except Piuserlogon.DoesNotExist as e:
            return None

    def Update(self, entity):
        """
        更新实体
        Args:
            userId (Piuserlogon): 实体
        Returns:
            returnValue (True or False): 更新成功或失败
        """
        try:
            entity.save()
            return True
        except:
            return False

    def GetUserDT(self):
        pass

    def GetStaffUserDT(self):
        pass

    def AccountActivation(self, userId, openId):
        """
        激活用户
        Args:
            userId (string): 用户主键
            openId (string): 唯一识别码
        Returns:
            returnValue (Piuser): 用户实体
        """
        returnCode = ''
        returnMessage = ''
        LogOnService.CheckOnLine()
        #用户没有找到状态
        returnCode = StatusCode.statusCodeDic['UserNotFound']
        #检查是否有效的合法的参数
        if openId:
            dataTable = Piuser.objects.filter(deletemark=0)
            if dataTable.count() == 1:
                userEntity = dataTable[0]
                #用户是否被锁定？
                if userEntity.enabled == 0:
                    returnCode = StatusCode.statusCodeDic['UserLocked']
                    return userEntity
                if userEntity.enabled == 1:
                    returnCode = StatusCode.statusCodeDic['UserIsActivate']
                    return userEntity
                if userEntity.enabled == -1:
                    returnCode = StatusCode.statusCodeDic['OK']
                    userEntity.enabled = 1
                    userEntity.save()
                    return userEntity


    def OnLine(self, userId, onLineState=1):
        """
        用户在线
        Args:
            userId (string): 用户主键
            onLineState (string): 用户在线状态
        Returns:
        """
        returnValue = 0
        if not SystemInfo.UpdateVisit:
            return returnValue
        returnValue = Piuserlogon.objects.filter(Q(id=userId)).update(useronline=onLineState)
        return returnValue

    def OnExit(self, userId):
        """
        用户离线
        Args:
            userId (string): 用户主键
        Returns:
        """
        returnValue = 0
        #是否更新访问日期信息
        if not SystemInfo.UpdateVisit:
            return returnValue

        returnValue = Piuserlogon.objects.filter(Q(id = userId)).update(previousvisit=F('lastvisit'), openid=uuid.uuid1(), useronline=0, lastvisit=datetime.datetime.now())
        return returnValue

    def ServerCheckOnLine(self):
        """
        服务器端检查在线状态
        Args:
        Returns:
            returnValue(int): 离线人数
        """
        returnValue = 0
        returnValue = LogOnService.CheckOnLine()
        return returnValue

    def SetPassword(self, userIds, password):
        """
        设置用户密码
        Args:
            userIds (string): 用户ID
            password (string): 密码
        Returns:
            returnValue(int): 大于0操作成功
        """
        returnValue = 0
        returnCode = ''
        returnMessage = ''
        enableCheckIPAddress = 0
        if not userIds or userIds.count() == 0:
            returnCode = StatusCode.statusCodeDic['NotFound']
            return returnCode,returnValue

        #设置密码
        if SystemInfo.EnableEncryptServerPassword:
            password = SecretHelper.AESEncrypt(self, password)

        if SystemInfo.EnableCheckIPAddress:
            enableCheckIPAddress = 1
        for id in userIds:
            Piuserlogon.objects.update_or_create(defaults={'id':id}, others={'checkipaddress':enableCheckIPAddress, 'userpassword':password, 'openid':uuid.uuid1()})
            returnValue = returnValue + 1
            returnCode = StatusCode.statusCodeDic['OK']
        return returnCode,returnValue

    def UserIsLogOn(self):
        pass

    def LockUser(self, userName):
        """
        锁定指定用户
        Args:
            userName (string): 用户名
        Returns:
            returnValue(int): 大于0操作成功
        """
        returnValue = 0
        try:
            user = Piuser.objects.get(Q(username=userName) & Q(enabled=1) & Q(deletemark=0))
            returnValue = Piuserlogon.objects.filter(id = user.id).update(lockstartdate=datetime.datetime.now(), lockenddate=(datetime.datetime.now() + datetime.timedelta(minutes=SystemInfo.PasswordErrorLockCycle)))
            return returnValue
        except Piuser.DoesNotExist as e:
            return returnValue

    def UnLockUser(self, userName):
        """
        解锁指定用户
        Args:
            userName (string): 用户名
        Returns:
            returnValue(int): 大于0操作成功
        """
        returnValue = 0
        try:
            user = Piuser.objects.get(Q(username=userName) & Q(enabled=1) & Q(deletemark=0))
            returnValue = Piuserlogon.objects.filter(id=user.id).update(lockstartdate=None, lockenddate=None)
            return returnValue
        except Piuser.DoesNotExist as e:
            return returnValue

    def UserDimission(self, userName, dimissionCause, dimissionDate, dimissionWhither=None):
        """
        用户离职
        Args:
            userName (string): 离职人员用户名
            dimissionCause (string): 离职原因
            dimissionDate (string): 离职日期
            dimissionWhither (string): 离职去向
        Returns:
            returnValue(int): 大于0操作成功
        """
        returnValue = 0
        userid = ''
        user = Piuser.objects.get(Q(username=userName) & Q(enabled=1) & Q(deletemark=0))
        returnValue = user.count()
        if returnValue > 0:
            user.update(enabled=0, isdimission=1, dimissioncause=dimissionCause, dimissionwhither=dimissionWhither, dimissiondate=dimissionDate)
            userid = user[0].id
            returnValue = returnValue + Piuserlogon.objects.filter(id=userid).update(lockstartdate=datetime.datetime.now())
        return returnValue

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

    def LogOn(userName, password, openId=None, createNewOpenId=False, ipAddress=None, macAddress=None, checkUserPassword=True):
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
        if SystemInfo.OnLineLimit > 0 and LogOnService.CheckOnLineLimit():
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
            if userEntity.auditstatus and userEntity.auditstatus.endswith(AuditStatus.WaitForAudit):
                ReturnStatusCode = AuditStatus.WaitForAudit
                return ReturnStatusCode,userInfo

            #用户无效、已离职的
            if userEntity.isdimission ==1 or userEntity.enabled ==0:
                ReturnStatusCode = StatusCode.statusCodeDic['LogOnDeny']
                return ReturnStatusCode,userInfo

            #用户是否有效的
            if userEntity.enabled == -1:
                ReturnStatusCode = StatusCode.statusCodeDic['UserNotActive']
                return ReturnStatusCode,userInfo

            userLogOnEntity = Piuserlogon.objects.get(id=userEntity.id)
            if (not userEntity.username) or (userEntity.username != 'Administrator'):
                #06. 允许登录时间是否有限制
                if userLogOnEntity.allowendtime:
                    userLogOnEntity.allowendtime = datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day, userLogOnEntity.allowendtime.hour, userLogOnEntity.allowendtime.minute, userLogOnEntity.allowendtime.second)
                if userLogOnEntity.allowstarttime:
                    userLogOnEntity.allowstarttime = datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day, userLogOnEntity.allowstarttime.hour, userLogOnEntity.allowstarttime.minute, userLogOnEntity.allowstarttime.second)
                    if datetime.datetime.now() < userLogOnEntity.allowstarttime:
                        ReturnStatusCode = StatusCode.statusCodeDic['UserLocked']
                        return ReturnStatusCode,userInfo
                if userLogOnEntity.allowendtime:
                    if datetime.datetime.now() > userLogOnEntity.allowendtime:
                        ReturnStatusCode = StatusCode.statusCodeDic['UserLocked']
                        return ReturnStatusCode,userInfo

                #07. 锁定日期是否有限制
                if userLogOnEntity.lockstartdate and datetime.datetime.now() > userLogOnEntity.lockstartdate:
                    if userLogOnEntity.lockenddate or datetime.datetime.now() < userLogOnEntity.lockenddate:
                        ReturnStatusCode = StatusCode.statusCodeDic['UserLocked']
                        return ReturnStatusCode,userInfo
        #08. 是否检查用户IP地址，是否进行访问限制？管理员不检查IP. && !this.IsAdministrator(userEntity.Id.ToString()
        if SystemInfo.EnableCheckIPAddress and userLogOnEntity.checkipAddress == 1 and (userEntity.username != 'Administrator' or userEntity.code == 'Administrator'):
            if ipAddress:
                if ParameterService.Exists(userEntity.id, 'IPAddress'):
                    if not CheckIPAddress.CheckIPAddress(ipAddress, userEntity.id):
                        ReturnStatusCode = StatusCode.statusCodeDic['ErrorIPAddress']
                        return ReturnStatusCode,userInfo

            #没有设置MAC地址时不检查
            if macAddress:
                if ParameterService.Exists(userEntity.id, 'MacAddress'):
                    if not CheckIPAddress.CheckIPAddress(macAddress, userEntity.id):
                        ReturnStatusCode = StatusCode.statusCodeDic['ErrorMacAddress']
                        return ReturnStatusCode,userInfo

        #10. 只允许登录一次，需要检查是否自己重新登录了，或者自己扮演自己了
        if UserInfo and UserInfo.Id != userEntity.id:
            if SystemInfo.CheckOnLine and userLogOnEntity.multiuserlogin == 0 and userLogOnEntity.useronline > 0:
                isSelf = False
                if openId:
                    if userLogOnEntity.openid:
                        if userLogOnEntity.openid == openId:
                            isSelf = True
                if not isSelf:
                    ReturnStatusCode = StatusCode.statusCodeDic['ErrorOnLine']
                    return ReturnStatusCode,userInfo

        #04. 系统是否采用了密码加密策略？
        if checkUserPassword and SystemInfo.EnableEncryptServerPassword:
            password = SecretHelper.AESEncrypt(password).decode()

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
                return ReturnStatusCode,userInfo

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

        userInfo = LogOnService.ConvertToUserInfo(userInfo, userEntity, userLogOnEntity)
        userInfo.IPAddress = ipAddress
        userInfo.MACAddress = macAddress
        userInfo.Password = password
        #这里是判断用户是否为系统管理员的
        userInfo.IsAdministrator = PermissionService.IsAdministrator(userEntity)
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
                userInfo.OpenId = LogOnService.UpdateVisitDate(userEntity.id, createNewOpenId)
            else:
                LogOnService.UpdateVisitDate(userEntity.id, createNewOpenId)
        return ReturnStatusCode,userInfo

    def CheckOnLineLimit(self):
        """
        检查用户在线状态(服务器专用)
        Args:
        Returns:
            returnValue(int): 影响行数
        """
        returnValue = False
        LogOnService.CheckOnLine()
        userOnLine = Piuserlogon.objects.filter(useronline__gt=0)
        if userOnLine and SystemInfo.OnLineLimit <= userOnLine.count():
            returnValue = True
        return returnValue

    def ConvertToUserInfo(userInfo, userEntity, userLogOnEntity):
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
        userInfo.RealName = userEntity.realname

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

    def UpdateVisitDate(userId, createOpenId = False):
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

    def ChangePassword(self, userId, oldPassword, newPassword):
        """
        更新密码
        Args:
            userId (string): 用户主键
            oldPassword (string): 老密码
            newPassword (string): 新密码
        Returns:
            returnValue (string): 影响行数
        """
        returnValue = 0
        statusCode = ''
        #密码强度检查
        if SystemInfo.EnableCheckPasswordStrength:
            if not newPassword:
                statusCode = StatusCode.statusCodeDic['PasswordCanNotBeNull']
                return statusCode,returnValue
            #最小长度、字母数字组合等强度检查
            if not ValidateUtil.EnableCheckPasswordStrength(self, newPassword):
                statusCode = StatusCode.statusCodeDic['PasswordNotStrength']
                return statusCode,returnValue

        #加密密码
        if SystemInfo.EnableEncryptServerPassword:
            oldPassword = SecretHelper.AESEncrypt(self, oldPassword)
            newPassword = SecretHelper.AESEncrypt(self, newPassword)

        #判断输入原始密码是否正确
        try:
            entity = Piuserlogon.objects.get(id = userId)
            if not entity.userpassword:
                entity.userpassword = ''

            if not entity.userpassword == oldPassword:
                statusCode = StatusCode.statusCodeDic['OldPasswordError']
                return statusCode,returnValue

            entity.userpassword = newPassword
            entity.changepassworddate = datetime.datetime.now()
            entity.save()
            statusCode = StatusCode.statusCodeDic['ChangePasswordOK']
            return statusCode, 1
        except Piuserlogon.DoesNotExist as e:
            pass


    def GetOnLineStateDT(self):
        sqlQuery = " SELECT " + 'piuserlogon' + "." + 'id' \
            + ", " + 'piuserlogon' + "." + 'useronline' \
            + " FROM " + 'piuserlogon' \
            + " WHERE " + 'piuserlogon' + "." + 'lastvisit' + " IS NOT NULL " \
            + " AND (DATEADD (s, " + str(SystemInfo.OnLineTime0ut + 5) + ", " + 'lastvisit' + ") > " + datetime.datetime.now() + ")"

        returnValue = DbCommonLibaray.executeQuery(None, sqlQuery)
        return returnValue
