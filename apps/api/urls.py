# _*_ coding: utf-8 _*_
__author__ = 'baxuelong@163.com'
__date__ = '2019/2/15 14:04'

from django.conf.urls import url
from spyne.server.django import DjangoView
from spyne.protocol.json import JsonDocument
from apps.api.views.LoginService import login_service,login_application,LoginService
from apps.api.views.UserAdminService import useradmin_service,useradmin_application,UserAdminService


urlpatterns = [
    url(r'^LoginService/', login_service),
    url(r'^LoginService_/', DjangoView.as_view(
        services=[LoginService],
        tns='Usable-Programming.LoginService.CheckLogin',
        in_protocol = JsonDocument(validator='soft'),
        out_protocol=JsonDocument())),
    url(r'^LoginService__/', DjangoView.as_view(application=login_application)),

    url(r'^UserAdminService/', useradmin_service),
    url(r'^UserAdminService_/', DjangoView.as_view(
        services=[UserAdminService],
        tns='Usable-Programming.UserAdminService',
        in_protocol = JsonDocument(validator='soft'),
        out_protocol=JsonDocument())),
    url(r'^UserAdminService__/', DjangoView.as_view(application=useradmin_application)),

]