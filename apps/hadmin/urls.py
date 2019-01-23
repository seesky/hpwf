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
import apps.hadmin.views.FramworkModules.LogAdminController_view as LogAdmin
import apps.hadmin.views.FramworkModules.ExceptionAdminController_view as ExceptionAdmin
import apps.hadmin.views.FramworkModules.DataItemAdminController_view as DataItemAdmin
import apps.hadmin.views.FramworkModules.ParameterAdminController_view as ParameterAdmin
import apps.hadmin.views.FramworkModules.SequenceAdminController_view as SequenceAdmin
import apps.hadmin.views.FramworkModules.TableFieldAdminController_view as TableFieldAdmin
import apps.hadmin.views.FramworkModules.UtilityController_view as Utility
import apps.hadmin.views.FramworkModules.PermissionSetController_view as PermissionSet
import apps.hadmin.views.FramworkModules.HighchartsController_view as Highcharts



urlpatterns = [
    url(r'^Index/', LoginController.Index),
    url(r'^CheckLogin/', LoginController.CheckLogin),
    url(r'^AccordionTreeIndex/', HomeController.AccordiontreeIndex),
    url(r'^LoadTreeMenu/', HomeController.LoadTreeMenu),
    url(r'^StartPage/', HomeController.StartPage),
    #
    url(r'^FrameworkModules/Utility/GetCategory/', Utility.GetCategory),
    url(r'^FrameworkModules/Utility/ExportExcel/', Utility.ExportExcel),
    #用户管理
    url(r'^FrameworkModules/UserAdmin/Index/', UserAdminController.Index),
    url(r'^FrameworkModules/UserAdmin/GetUserPageDTByDepartmentId/', UserAdminController.GetUserPageDTByDepartmentId),
    url(r'^FrameworkModules/UserAdmin/GetUserListByPage/', UserAdminController.GetUserListByPage),
    url(r'^FrameworkModules/UserAdmin/Form/', UserAdminController.Form),
    url(r'^FrameworkModules/UserAdmin/SubmitForm/', UserAdminController.SubmitForm),
    url(r'^FrameworkModules/UserAdmin/GetEntity/', UserAdminController.GetEntity),
    url(r'^FrameworkModules/UserAdmin/Delete/', UserAdminController.Delete),
    url(r'^FrameworkModules/UserAdmin/SetUserPassword/', UserAdminController.SetUserPassword),
    url(r'^FrameworkModules/UserAdmin/UserDimission/', UserAdminController.UserDimission),
    url(r'^FrameworkModules/UserAdmin/SetUserDimission/', UserAdminController.SetUserDimission),
    url(r'^FrameworkModules/UserAdmin/GetUserListJson/', UserAdminController.GetUserListJson),
    url(r'^FrameworkModules/UserAdmin/GetDTByRole/', UserAdminController.GetDTByRole),
    #组织机构管理
    url(r'^FrameworkModules/OrganizeAdmin/Index/', OrganizeAdmin.Index),
    url(r'^FrameworkModules/OrganizeAdmin/GetOrganizeTreeJson/', OrganizeAdmin.GetOrganizeTreeJson),
    url(r'^FrameworkModules/OrganizeAdmin/GetOrganizeByCategory/', OrganizeAdmin.GetOrganizeByCategory),
    url(r'^FrameworkModules/OrganizeAdmin/Form/', OrganizeAdmin.Form),
    url(r'^FrameworkModules/OrganizeAdmin/SubmitForm/', OrganizeAdmin.SubmitForm),
    url(r'^FrameworkModules/OrganizeAdmin/GetEntity/', OrganizeAdmin.GetEntity),
    url(r'^FrameworkModules/OrganizeAdmin/Delete/', OrganizeAdmin.Delete),
    url(r'^FrameworkModules/OrganizeAdmin/MoveTo/', OrganizeAdmin.MoveTo),
    #员工管理
    url(r'^FrameworkModules/StaffAdmin/Index/', StaffAdmin.Index),
    url(r'^FrameworkModules/StaffAdmin/GetStaffByOrganizeId/', StaffAdmin.GetStaffByOrganizeId),
    url(r'^FrameworkModules/StaffAdmin/Form/', StaffAdmin.Form),
    url(r'^FrameworkModules/StaffAdmin/SubmitForm/', StaffAdmin.SubmitForm),
    url(r'^FrameworkModules/StaffAdmin/GetEntity/', StaffAdmin.GetEntity),
    url(r'^FrameworkModules/StaffAdmin/Delete/', StaffAdmin.Delete),
    url(r'^FrameworkModules/StaffAdmin/MoveTo/', StaffAdmin.MoveTo),
    #角色管理
    url(r'^FrameworkModules/RoleAdmin/Index/', RoleAdmin.Index),
    url(r'^FrameworkModules/RoleAdmin/GridPageListJson/', RoleAdmin.GridPageListJson),
    url(r'^FrameworkModules/RoleAdmin/GetRoleListByOrganize/', RoleAdmin.GetRoleListByOrganize),
    url(r'^FrameworkModules/RoleAdmin/GetRoleCategory/', RoleAdmin.GetRoleCategory),
    url(r'^FrameworkModules/RoleAdmin/GetEnabledRoleList/', RoleAdmin.GetEnabledRoleList),
    url(r'^FrameworkModules/RoleAdmin/Form/', RoleAdmin.Form),
    url(r'^FrameworkModules/RoleAdmin/SubmitForm/', RoleAdmin.SubmitForm),
    url(r'^FrameworkModules/RoleAdmin/GetEntity/', RoleAdmin.GetEntity),
    url(r'^FrameworkModules/RoleAdmin/Delete/', RoleAdmin.Delete),
    url(r'^FrameworkModules/RoleAdmin/AddUserToRole/', RoleAdmin.AddUserToRole),
    url(r'^FrameworkModules/RoleAdmin/RemoveUserFromRole/', RoleAdmin.RemoveUserFromRole),
    url(r'^FrameworkModules/RoleAdmin/GetRoleList/', RoleAdmin.GetRoleList),
    #岗位管理
    url(r'^FrameworkModules/PostAdmin/Index/', PostAdmin.Index),
    url(r'^FrameworkModules/PostAdmin/Form/', PostAdmin.Form),
    url(r'^FrameworkModules/PostAdmin/SubmitForm/', PostAdmin.SubmitForm),
    url(r'^FrameworkModules/PostAdmin/GetEntity/', PostAdmin.GetEntity),
    url(r'^FrameworkModules/PostAdmin/Delete/', PostAdmin.Delete),
    url(r'^FrameworkModules/PostAdmin/MoveTo/', PostAdmin.MoveTo),


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
    url(r'^FrameworkModules/LogAdmin/Index/', LogAdmin.Index),
    url(r'^FrameworkModules/LogAdmin/GridPageListJson/', LogAdmin.GridPageListJson),
    url(r'^FrameworkModules/ExceptionAdmin/Index/', ExceptionAdmin.Index),
    url(r'^FrameworkModules/ExceptionAdmin/GridPageListJson/', ExceptionAdmin.GridPageListJson),
    url(r'^FrameworkModules/DataItemAdmin/Index/', DataItemAdmin.Index),
    url(r'^FrameworkModules/DataItemAdmin/GetDataItemTreeJson/', DataItemAdmin.GetDataItemTreeJson),
    url(r'^FrameworkModules/DataItemAdmin/GetDataItemDetailById/', DataItemAdmin.GetDataItemDetailById),
    url(r'^FrameworkModules/ParameterAdmin/Index/', ParameterAdmin.Index),
    url(r'^FrameworkModules/ParameterAdmin/GridPageListJson/', ParameterAdmin.GridPageListJson),
    url(r'^FrameworkModules/SequenceAdmin/GridPageListJson/', SequenceAdmin.GridPageListJson),
    url(r'^FrameworkModules/SequenceAdmin/Index/', SequenceAdmin.Index),
    url(r'^FrameworkModules/TableFieldAdmin/Index/', TableFieldAdmin.Index),
    url(r'^FrameworkModules/TableFieldAdmin/GetTableNameAndCode/', TableFieldAdmin.GetTableNameAndCode),
    url(r'^FrameworkModules/TableFieldAdmin/GetDTByTable/', TableFieldAdmin.GetDTByTable),
    #权限设置
    url(r'^FrameworkModules/PermissionSet/RoleUserSet/', PermissionSet.RoleUserSet),
    url(r'^FrameworkModules/PermissionSet/PermissionBacthSet/', PermissionSet.PermissionBacthSet),
    url(r'^FrameworkModules/PermissionSet/GetPermissionScopeTargetIds/', PermissionSet.GetPermissionScopeTargetIds),
    url(r'^FrameworkModules/PermissionSet/GrantRevokePermissionScopeTargets/', PermissionSet.GrantRevokePermissionScopeTargets),
    url(r'^FrameworkModules/PermissionSet/RolePermissionSet/', PermissionSet.RolePermissionSet),
    url(r'^FrameworkModules/PermissionSet/GetModuleByRoleId/', PermissionSet.GetModuleByRoleId),
    url(r'^FrameworkModules/PermissionSet/GetPermissionItemsByRoleId/', PermissionSet.GetPermissionItemsByRoleId),
    url(r'^FrameworkModules/PermissionSet/SetRoleModulePermission/', PermissionSet.SetRoleModulePermission),
    url(r'^FrameworkModules/PermissionSet/SetRolePermissionItem/', PermissionSet.SetRolePermissionItem),

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