# _*_ coding: utf-8 _*_
__author__ = 'baxuelong@163.com'
__date__ = '2018/12/11 15:01'

class AuditStatus(object):

    #00 草稿状态
    Draft = 0

    #01 开始审核
    StartAudit = 1

    #02 审核通过
    AuditPass = 2

    #03 待审核
    WaitForAudit = 3

    #04 转发
    Transit = 4

    #05 已退回
    AuditReject = 5

    #06 审核结束
    AuditComplete = 6

    #07 撤销,废弃
    AuditQuash = 7