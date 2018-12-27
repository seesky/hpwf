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