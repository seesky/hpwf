# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2019/1/4 11:06'
from django.conf.urls import url
import apps.hadmin.views.LoginController_view as LoginController
import apps.hadmin.views.HomeController_view as HomeController
import apps.hadmin.views.FramworkModules.UserAdminController_view as UserAdminController

urlpatterns = [
    url(r'^index/', LoginController.index),
    url(r'^checklogin/', LoginController.checklogin),
    url(r'^accordiontreeindex/', HomeController.accordiontreeindex),
    url(r'^loadtreemenu/', HomeController.loadtreemenu),
    url(r'^startpage/', HomeController.startpage),
    url(r'^frameworkmodules/useradmin/index/', UserAdminController.index),
]