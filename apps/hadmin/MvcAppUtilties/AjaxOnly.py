# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2019/1/8 16:55'

from django.core.exceptions import PermissionDenied

class AjaxOnly(object):

    def __init__(self, func):
        self.f = func

    def __call__(self, request):

        if request.is_ajax():
            return self.f(request)
        else:
            raise PermissionDenied()