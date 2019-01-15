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
import apps.hadmin.views.FramworkModules.MessageAdminController_view as MessageAdmin
import apps.hadmin.views.FramworkModules.HighchartsController_view as Highcharts

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
    url(r'^FrameworkModules/MessageAdmin/Index/', MessageAdmin.Index),
    url(r'^FrameworkModules/MessageAdmin/GetMessageListByFunctionCode/', MessageAdmin.GetMessageListByFunctionCode),

    url(r'^FrameworkModules/Highcharts/Sample1/', Highcharts.Sample1),
    url(r'^FrameworkModules/Highcharts/Sample2/', Highcharts.Sample2),
    url(r'^FrameworkModules/Highcharts/Sample3/', Highcharts.Sample3),
    url(r'^FrameworkModules/Highcharts/Sample4/', Highcharts.Sample4),
    url(r'^FrameworkModules/Highcharts/Sample5/', Highcharts.Sample5),
    url(r'^FrameworkModules/Highcharts/Sample6/', Highcharts.Sample6),
    url(r'^FrameworkModules/Highcharts/Sample7/', Highcharts.Sample7),
    url(r'^FrameworkModules/Highcharts/Sample8/', Highcharts.Sample8),
    url(r'^FrameworkModules/Highcharts/Sample9/', Highcharts.Sample9),
    url(r'^FrameworkModules/Highcharts/Sample10/', Highcharts.Sample10),
    url(r'^FrameworkModules/Highcharts/Sample11/', Highcharts.Sample11),
    url(r'^FrameworkModules/Highcharts/Sample12/', Highcharts.Sample12),
    url(r'^FrameworkModules/Highcharts/Sample13/', Highcharts.Sample13),
    url(r'^FrameworkModules/Highcharts/Sample14/', Highcharts.Sample14),
    url(r'^FrameworkModules/Highcharts/Sample15/', Highcharts.Sample15),
    url(r'^FrameworkModules/Highcharts/Sample16/', Highcharts.Sample16),
    url(r'^FrameworkModules/Highcharts/Sample17/', Highcharts.Sample17),
    url(r'^FrameworkModules/Highcharts/Sample18/', Highcharts.Sample18),
    url(r'^FrameworkModules/Highcharts/Sample19/', Highcharts.Sample19),
    url(r'^FrameworkModules/Highcharts/Sample20/', Highcharts.Sample20),
    url(r'^FrameworkModules/Highcharts/Sample21/', Highcharts.Sample21),
    url(r'^FrameworkModules/Highcharts/Sample22/', Highcharts.Sample22),
    url(r'^FrameworkModules/Highcharts/Sample23/', Highcharts.Sample23),
    url(r'^FrameworkModules/Highcharts/Sample24/', Highcharts.Sample24),
    url(r'^FrameworkModules/Highcharts/Sample25/', Highcharts.Sample25),
    url(r'^FrameworkModules/Highcharts/Sample26/', Highcharts.Sample26),
    url(r'^FrameworkModules/Highcharts/Sample27/', Highcharts.Sample27),
    url(r'^FrameworkModules/Highcharts/Sample28/', Highcharts.Sample28),
    url(r'^FrameworkModules/Highcharts/Sample29/', Highcharts.Sample29),


]