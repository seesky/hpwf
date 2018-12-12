# _*_ coding: utf-8 _*_
__author__ : 'seesky@hstecs.com'
__date__ : '2018/12/12 15:56'

from enum import Enum

class StatusCode(object):

    statusCodeDic = {
        'DbError': 0,
        'Error': 9,  # 09发生错误。
        'OK': 10,  # 10运行成功。
        'OKAdd': 11,  # 11添加成功。
        'CanNotLock': 12,  # 12不能锁定数据。
        'LockOK': 13,  # 13成功锁定数据。
        'OKUpdate': 14,  # 14更新数据成功。
        'OKDelete': 15,  # 15删除成功。
        'Exist': 16,  # 16数据已重复, 不可以重复。
        'ErrorCodeExist': 17,  # 17编号已存在, 不可以重复。
        'ErrorNameExist': 18,  # 18名称已重复
        'ErrorValueExist': 19,  # 19值已重复
        'ErrorUserExist': 20,  # 20用户名已重复
        'ErrorDataRelated': 22,  # 22数据已经被引用，有关联数据在。
        'ErrorDeleted': 23,  # 23数据已被其他人删除。
        'ErrorChanged': 24,  # 24数据已被其他人修改。
        'NotFound': 25,  # 25为找到记录。
        'UserNotFound': 26,  # 26用户没有找到。
        'PasswordError': 27,  # 27密码错误。
        'LogOnDeny': 28,  # 28登录被拒绝。
        'ErrorOnLine': 29,  # 29只允许登录一次
        'ErrorMacAddress': 30,  # 30是否检查用户的网卡Mac地址
        'ErrorIPAddress': 31,  # 31是否检查用户IP地址
        'ErrorOnLineLimit': 32,  # 32同时在线用户数量限制
        'PasswordCanNotBeNull': 33,  # 33密码不允许为空。
        'SetPasswordOK': 34,  # 34设置密码成功。
        'OldPasswordError': 35,  # 35原密码错误。
        'ChangePasswordOK': 36,  # 36修改密码成功。
        'UserNotEmail': 37,  # 37用户没有电子邮件地址。
        'UserLocked': 38,  # 38用户被锁定。
        'UserNotActive': 39,  # 39用户还未被激活。
        'UserIsActivate': 40,  # 40用户已被激活，不用重复激活。
        'ErrorLogOn': 41,  # 41用户名或密码错误。
        'WaitForAudit': 42,  # 42用户还在待审核状态。
        'UserDuplicate': 43,  # 43用户还在待审核状态。
        'StartAudit': 44,  # 44启动成功。
        'PasswordNotStrength': 45  # 45密码不够强

    }
