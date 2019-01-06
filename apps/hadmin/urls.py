# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2019/1/4 11:06'
from django.conf.urls import url
import apps.hadmin.views.LoginController_view as LoginController

urlpatterns = [
    url(r'^index/', LoginController.index),
    url(r'^checklogin/', LoginController.checklogin),
]