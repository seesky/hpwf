# _*_ coding: utf-8 _*_
__author__ = 'baxuelong@163.com'
__date__ = '2019/2/28 8:30'

from django.conf.urls import url
import apps.front.views.FrontController_views as FrontAdmin

urlpatterns = [
    url(r'^Index/', FrontAdmin.Index),
    url(r'^IndexManage/', FrontAdmin.IndexManage),
]