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
import apps.hadmin.views.FramworkModules.PostAdminController_view as PostAdmin
import apps.hadmin.views.FramworkModules.ModuleAdminController_view as ModuleAdmin
import apps.hadmin.views.FramworkModules.PermissionItemAdminController_views as PermissionItem
import apps.hadmin.views.FramworkModules.UserPermissionAdminController_views as UserPermission
import apps.hadmin.views.FramworkModules.RolePermissionAdminController_views as RolePermission

urlpatterns = [
    url(r'^Index/', LoginController.Index),
    url(r'^CheckLogin/', LoginController.CheckLogin),
    url(r'^AccordionTreeIndex/', HomeController.AccordiontreeIndex),
    url(r'^LoadTreeMenu/', HomeController.LoadTreeMenu),
    url(r'^StartPage/', HomeController.StartPage),
    url(r'^FrameworkModules/UserAdmin/Index/', UserAdminController.Index),
    url(r'^FrameworkModules/UserAdmin/GetUserPageDTByDepartmentId/', UserAdminController.GetUserPageDTByDepartmentId),
    url(r'^FrameworkModules/UserAdmin/GetUserListByPage/', UserAdminController.GetUserListByPage),
    url(r'^FrameworkModules/OrganizeAdmin/Index/', OrganizeAdmin.Index),
    url(r'^FrameworkModules/OrganizeAdmin/GetOrganizeTreeJson/', OrganizeAdmin.GetOrganizeTreeJson),
    url(r'^FrameworkModules/StaffAdmin/Index/', StaffAdmin.Index),
    url(r'^FrameworkModules/StaffAdmin/GetStaffByOrganizeId/', StaffAdmin.GetStaffByOrganizeId),
    url(r'^FrameworkModules/RoleAdmin/Index/', RoleAdmin.Index),
    url(r'^FrameworkModules/RoleAdmin/GridPageListJson/', RoleAdmin.GridPageListJson),
    url(r'^FrameworkModules/RoleAdmin/GetRoleListByOrganize/', RoleAdmin.GetRoleListByOrganize),
    url(r'^FrameworkModules/RoleAdmin/GetRoleCategory/', RoleAdmin.GetRoleCategory),
    url(r'^FrameworkModules/PostAdmin/Index/', PostAdmin.Index),
    url(r'^FrameworkModules/ModuleAdmin/Index/', ModuleAdmin.Index),
    url(r'^FrameworkModules/ModuleAdmin/GetModuleTreeJson/', ModuleAdmin.GetModuleTreeJson),
    url(r'^FrameworkModules/ModuleAdmin/GetModuleByIds/', ModuleAdmin.GetModuleByIds),
    url(r'^FrameworkModules/PermissionItemAdmin/Index/', PermissionItem.Index),
    url(r'^FrameworkModules/PermissionItemAdmin/GetPermissionItemTreeJson/', PermissionItem.GetPermissionItemTreeJson),
    url(r'^FrameworkModules/PermissionItemAdmin/GetPermissionItemByIds/', PermissionItem.GetPermissionItemByIds),
    url(r'^FrameworkModules/UserPermissionAdmin/Index/', UserPermission.Index),
    url(r'^FrameworkModules/RolePermissionAdmin/Index/', RolePermission.Index),
]