# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2018/12/26 14:03'

from apps.utilities.publiclibrary.SystemInfo import SystemInfo
from apps.utilities.publiclibrary.MachineInfoHelper import MachineInfoHelper

class UserInfo(object):
    #用户主键
    Id = None

    #用户用户名
    UserName = None

    #用户姓名
    RealName = None

    #当前的组织结构公司主键
    CompanyId = None

    #远程调用Service密码（为了提高软件的安全性）
    ServicePassword = None

    #远程调用Service用户名（为了提高软件的安全性）
    ServiceUsername = None

    #默认角色
    RoleId = None

    #当前的组织结构工作组主键
    WorkgroupId = None

    #当前的组织结构子公司主键
    SubCompanyId = None

    #当前语言选择
    CurrentLanguage = None

    #当前布局风格选择
    Themes = None

    #IP地址
    IPAddress = None

    #MAC地址
    MACAddress = None

    #单点登录唯一识别标识
    OpenId = None

    #目标用户
    TargetUserId = None

    #员工主键
    StaffId = None

    #编号
    Code = None

    #当前的组织结构公司编号
    CompanyCode = None

    #当前的组织结构公司名称
    CompanyName = None

    #当前的组织结构子公司名称
    SubCompanyName = None

    #当前的组织结构子公司编号
    SubCompanyCode = None

    #当前的组织结构部门主键
    DepartmentId = None

    #当前的组织结构部门编号
    DepartmentCode = None

    #当前的组织结构部门名称
    DepartmentName = None

    #当前的组织结构工作组编号
    WorkgroupCode = None

    #当前的组织结构工作组名称
    WorkgroupName = None

    #安全级别
    SecurityLevel = None

    #默认角色名称
    RoleName = None

    #是否超级管理员
    IsAdministrator = None

    #密码
    Password = None

    #进程名称
    ProcessName = None

    #进程ID
    ProcessId = None

    #最后一次访问时间
    LastVisit = None


    def __init__(self):
        self.CompanyId = None
        self.ServicePassword = SystemInfo.ServiceUserName
        self.ServiceUsername = SystemInfo.ServicePassword
        self.CurrentLanguage = SystemInfo.CurrentLanguage
        self.Themes = SystemInfo.Themes
        self.SecurityLevel = 0
        self.RoleId = None
        self.WorkgroupId = None
        self.DepartmentId = None
        self.SubCompanyId = None
        self.IPAddress = MachineInfoHelper.GetIPAddress(self)
        self.MACAddress = MachineInfoHelper.GetMacAddress(self)
        self.Id = MachineInfoHelper.GetHostname(self)
        self.RealName = MachineInfoHelper.GetHostname(self)