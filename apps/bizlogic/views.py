import datetime
from django.shortcuts import render
from django.views.generic.base import View
from .models import Piuser
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from apps.bizlogic.service.base.UserService import UserSerivce
from apps.bizlogic.service.base.UserService import UserSerivce

# Create your views here.

class PiuserTest(View):
    def get(self, request):
        roleIds = ['D25198E7-84E7-4C1A-8EA9-C047D2A13FBF']
        # #userPage = UserSerivce.GetDTByPage(self, '', '07DF66FA-644E-4B1F-9994-AE7332796058', '27A40BF7-D68C-4BF5-9B40-056A8D3E9A81', 2, None)
        userList = UserSerivce.HSearch(self, '', '', roleIds)
        return HttpResponse(len(userList))

