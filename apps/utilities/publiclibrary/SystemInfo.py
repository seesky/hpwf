# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2018/12/26 14:09'

class SystemInfo(object):
    ServiceUserName = 'HPWFFramework'
    ServicePassword = 'HPWFFramework123456'
    CurrentLanguage = 'zh-CN'
    Themes = ''

    #是否更新访问日期信息
    UpdateVisit = True

    #检查周期[以秒为单位]2分钟内不在线的，就认为是已经没在线了，心跳方式检查
    OnLineTime0ut = 2 * 60 + 20

    #同时在线用户数量限制
    OnLineLimit = 0

    #检查密码强度
    EnableCheckPasswordStrength = False

    #是否检查用户IP地址
    EnableCheckIPAddress = False

    #禁止用户重复登录,只允许登录一次
    CheckOnLine = False

    #服务器端加密存储密码
    EnableEncryptServerPassword = True

    #密码错误锁定次数
    PasswordErrorLockLimit = 5

    #连续输入N次密码后，密码错误锁定周期(分钟),0 表示 需要系统管理员进行审核，帐户直接被设置为无效
    PasswordErrorLockCycle = 30

    #检查密码强度
    EnableCheckPasswordStrength = False

    #是否更新访问日期信息
    UpdateVisit = True

    #启用组织机构权限
    EnableOrganizePermission = False