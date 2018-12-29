# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2018/12/19 16:59'

class PermissionScope(object):
    PermissionScopeDic = {
        'No' : 0,#没有任何数据权限
        'All' : -1, # 全部数据
        'UserCompany' : -2, # 用户所在公司数据
        'UserSubOrg' : -3, # 用户所在分支机构数据
        'UserDepartment' : -4, # 用户所在部门数据
        'UserWorkgroup' : -5, # 用户所在工作组数据
        'User' : -6, # 自己的数据，仅本人
        'Detail' : -7 # 按详细设定的数据
    }
