# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2019/1/4 11:06'
from django.conf.urls import url
import apps.hadmin.views.LoginController_view as LoginController
import apps.hadmin.views.HomeController_view as HomeController
import apps.hadmin.views.FramworkModules.UserAdminController_view as UserAdminController
import apps.hadmin.views.FramworkModules.OrganizeAdminController_view as OrganizeAdmin
import apps.hadmin.views.FramworkModules.StaffAdminController_view as StaffAdmin
import apps.hadmin.views.FramworkModules.RoleAdminController_view as RoleAdmin

urlpatterns = [
    url(r'^Index/', LoginController.Index),
    url(r'^CheckLogin/', LoginController.CheckLogin),
    url(r'^AccordionTreeIndex/', HomeController.AccordiontreeIndex),
    url(r'^LoadTreeMenu/', HomeController.LoadTreeMenu),
    url(r'^StartPage/', HomeController.StartPage),
    url(r'^FrameworkModules/UserAdmin/Index/', UserAdminController.Index),
    url(r'^FrameworkModules/UserAdmin/GetUserPageDTByDepartmentId/', UserAdminController.GetUserPageDTByDepartmentId),
    url(r'^FrameworkModules/OrganizeAdmin/GetOrganizeTreeJson/(?P<isTree>\d+)/', OrganizeAdmin.GetOrganizeTreeJson),
    url(r'^FrameworkModules/StaffAdmin/Index/', StaffAdmin.Index),
    url(r'^FrameworkModules/StaffAdmin/GetStaffByOrganizeId/', StaffAdmin.GetStaffByOrganizeId),
    url(r'^FrameworkModules/RoleAdmin/Index/', RoleAdmin.Index),
    url(r'^FrameworkModules/RoleAdmin/GridPageListJson/', RoleAdmin.GridPageListJson),
    url(r'^FrameworkModules/RoleAdmin/GetRoleCategory/', RoleAdmin.GetRoleCategory),
]