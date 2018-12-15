import datetime
from django.shortcuts import render
from django.views.generic.base import View
from .models import Piuser
from .models import Piuserrole
from .models import Pipermission
from .models import Pipermissionscope


from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from apps.bizlogic.service.base.UserService import UserSerivce
from apps.bizlogic.service.base.UserService import UserSerivce


# Create your views here.

class PiuserTest(View):
    def get(self, request):
        roleIds = ['15D7E70A-CE55-4CE2-B6E2-8025810C5C16']
        idsTrue = ['0003d3f5-6aa1-4475-adf6-50961c8bd739','0003d3f5-6aa1-4475-adf6-50961c8bd731']
        ids = ['0009ed41-3753-4f99-b52d-4ea6a43dda1a','0003d3f5-6aa1-4475-adf6-50961c8bd739']
        # #userPage = UserSerivce.GetDTByPage(self, '', '07DF66FA-644E-4B1F-9994-AE7332796058', '27A40BF7-D68C-4BF5-9B40-056A8D3E9A81', 2, None)
        #userList = UserSerivce.Search(self, '', '', roleIds)
        #userList = UserSerivce.SetUserAuditStates(self, ids, None)





        returnValue = UserSerivce.BatchDelete(self, idsTrue)
        return HttpResponse(returnValue)

