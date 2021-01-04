# _*_ coding: utf-8 _*_
__author__ = 'baxuelong@163.com'
__date__ = '2019/1/18 8:49'

class ConstrainUtil(object):

    ParameterReference = "当前用户主键：用户主键（CurrentUserId）\
                                                    当前用户编号：用户编号（CurrentUserCode）\
                                                    当前用户名  ：用户名（CurrentUserName）\
                                                    当前用户姓名：用户姓名（CurrentRealName）\
                                                    所在公司主键：公司主键（CurrentCompanyId）\
                                                    所在公司名称：公司名称（CurrentCompanyName）\
                                                    所在公司编号：公司编号（CurrentCompanyCode）\
                                                    所在部门主键：部门主键（CurrentDepartmentId）\
                                                    所在部门名称：部门名称（CurrentDepartmentName）\
                                                    所在部门编号：部门编号（CurrentDepartmentCode）\
                                                    所在工作组主键：工作组主键（CurrentWorkgroupId）\
                                                    所在工作组名称：工作组名称（CurrentWorkgroupName）\
                                                    所在工作组编号：工作组编号（CurrentWorkgroupCode）"

    def PrepareParameter(userInfo, constraint):
        constraint = constraint.replace("用户主键", userInfo.Id)
        constraint = constraint.replace("CurrentUserId", userInfo.Id)
        constraint = constraint.replace("用户编号", userInfo.Code)
        constraint = constraint.replace("CurrentUserCode", userInfo.Code)
        constraint = constraint.replace("用户名", userInfo.UserName)
        constraint = constraint.replace("CurrentUserName", userInfo.UserName)
        constraint = constraint.replace("用户姓名", userInfo.RealName)
        constraint = constraint.replace("CurrentRealName", userInfo.RealName)
        constraint = constraint.replace("公司主键", userInfo.CompanyId)
        constraint = constraint.replace("CurrentCompanyId", userInfo.CompanyId)
        constraint = constraint.replace("部门主键", userInfo.DepartmentId)
        constraint = constraint.replace("CurrentDepartmentId", userInfo.DepartmentId)
        constraint = constraint.replace("工作组主键", userInfo.WorkgroupId)
        constraint = constraint.replace("CurrentWorkgroupId", userInfo.WorkgroupId)
        return constraint