# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2018/12/26 14:03'

from apps.utilities.publiclibrary.SystemInfo import SystemInfo
from apps.utilities.publiclibrary.MachineInfoHelper import MachineInfoHelper

class UserInfo(object):
    #用户主键
    Id = ''

    #用户用户名
    UserName = ''

    #用户姓名
    RealName = ''

    #当前的组织结构公司主键
    CompanyId = ''

    #远程调用Service密码（为了提高软件的安全性）
    ServicePassword = ''

    #远程调用Service用户名（为了提高软件的安全性）
    ServiceUsername = ''

    #默认角色
    RoleId = ''

    #当前的组织结构工作组主键
    WorkgroupId = ''

    #当前的组织结构子公司主键
    SubCompanyId = ''

    #当前语言选择
    CurrentLanguage = ''

    #当前布局风格选择
    Themes = ''

    #IP地址
    IPAddress = ''

    #MAC地址
    MACAddress = ''

    #单点登录唯一识别标识
    OpenId = ''

    #目标用户
    TargetUserId = ''

    #员工主键
    StaffId = ''

    #编号
    Code = ''

    #当前的组织结构公司编号
    CompanyCode = ''

    #当前的组织结构公司名称
    CompanyName = ''

    #当前的组织结构子公司名称
    SubCompanyName = ''

    #当前的组织结构子公司编号
    SubCompanyCode = ''

    #当前的组织结构部门主键
    DepartmentId = ''

    #当前的组织结构部门编号
    DepartmentCode = ''

    #当前的组织结构部门名称
    DepartmentName = ''

    #当前的组织结构工作组编号
    WorkgroupCode = ''

    #当前的组织结构工作组名称
    WorkgroupName = ''

    #安全级别
    SecurityLevel = ''

    #默认角色名称
    RoleName = ''

    #是否超级管理员
    IsAdministrator = ''

    #密码
    Password = ''

    #进程名称
    ProcessName = ''

    #进程ID
    ProcessId = ''

    #最后一次访问时间
    LastVisit = ''


    def __init__(self):
        self.CompanyId = ''
        self.ServicePassword = SystemInfo.ServiceUserName
        self.ServiceUsername = SystemInfo.ServicePassword
        self.CurrentLanguage = SystemInfo.CurrentLanguage
        self.Themes = SystemInfo.Themes
        self.SecurityLevel = 0
        self.RoleId = ''
        self.WorkgroupId = ''
        self.DepartmentId = ''
        self.SubCompanyId = ''
        self.IPAddress = MachineInfoHelper.GetIPAddress(self)
        self.MACAddress = MachineInfoHelper.GetMacAddress(self)
        self.Id = MachineInfoHelper.GetHostname(self)
        self.RealName = MachineInfoHelper.GetHostname(self)

    def obj_2_json(obj):
        return {
            'Id' : obj.Id,
            'UserName' :obj.UserName,
            'RealName' :obj.RealName,
            'CompanyId' :obj.CompanyId,
            'ServicePassword' :obj.ServicePassword,
            'ServiceUsername' :obj.ServiceUsername,
            'RoleId' :obj.RoleId,
            'WorkgroupId' :obj.WorkgroupId,
            'SubCompanyId' :obj.SubCompanyId,
            'CurrentLanguage' :obj.CurrentLanguage,
            'Themes' :obj.Themes,
            'IPAddress' :obj.IPAddress,
            'MACAddress' :obj.MACAddress,
            'OpenId' :obj.OpenId,
            'TargetUserId' :obj.TargetUserId,
            'StaffId' :obj.StaffId,
            'Code' :obj.Code,
            'CompanyCode' :obj.CompanyCode,
            'CompanyName' :obj.CompanyName,
            'SubCompanyName' :obj.SubCompanyName,
            'SubCompanyCode' :obj.SubCompanyCode,
            'DepartmentId' :obj.DepartmentId,
            'DepartmentCode' :obj.DepartmentCode,
            'DepartmentName' :obj.DepartmentName,
            'WorkgroupCode' :obj.WorkgroupCode,
            'WorkgroupName' :obj.WorkgroupName,
            'SecurityLevel' :obj.SecurityLevel,
            'RoleName' :obj.RoleName,
            'IsAdministrator' :obj.IsAdministrator,
            'Password' :obj.Password,
            'ProcessName' :obj.ProcessName,
            'ProcessId' :obj.ProcessId,
            'LastVisit' :obj.LastVisit
        }

    def json_2_obj(d):
        userInfo = UserInfo()
        userInfo.Id = d['Id']
        userInfo.UserName = d['UserName']
        userInfo.RealName = d['RealName']
        userInfo.CompanyId = d['CompanyId']
        userInfo.ServicePassword = d['ServicePassword']
        userInfo.ServiceUsername = d['ServiceUsername']
        userInfo.RoleId = d['RoleId']
        userInfo.WorkgroupId = d['WorkgroupId']
        userInfo.SubCompanyId = d['SubCompanyId']
        userInfo.CurrentLanguage = d['CurrentLanguage']
        userInfo.Themes = d['Themes']
        userInfo.IPAddress = d['IPAddress']
        userInfo.MACAddress = d['MACAddress']
        userInfo.OpenId = d['OpenId']
        userInfo.TargetUserId = d['TargetUserId']
        userInfo.StaffId = d['StaffId']
        userInfo.Code = d['Code']
        userInfo.CompanyCode = d['CompanyCode']
        userInfo.CompanyName = d['CompanyName']
        userInfo.SubCompanyName = d['SubCompanyName']
        userInfo.SubCompanyCode = d['SubCompanyCode']
        userInfo.DepartmentId = d['DepartmentId']
        userInfo.DepartmentCode = d['DepartmentCode']
        userInfo.DepartmentName = d['DepartmentName']
        userInfo.WorkgroupCode = d['WorkgroupCode']
        userInfo.WorkgroupName = d['WorkgroupName']
        userInfo.SecurityLevel = d['SecurityLevel']
        userInfo.RoleName = d['RoleName']
        userInfo.IsAdministrator = d['IsAdministrator']
        userInfo.Password = d['Password']
        userInfo.ProcessName = d['ProcessName']
        userInfo.ProcessId = d['ProcessId']
        userInfo.LastVisit = d['LastVisit']
        return userInfo