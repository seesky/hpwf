import datetime
from django.shortcuts import render
from django.views.generic.base import View
from .models import Piuser
from .models import Piuserrole
from .models import Pipermission
from .models import Pipermissionscope
from django.db.models import Q
import uuid


from django.http import HttpResponse

from apps.bizlogic.service.base.UserOrganizeSerivce import UserOrganizeService




# Create your views here.

class PiuserTest(View):
    def get(self, request):

        returnValue = UserOrganizeService.UserIsInOrganize(self, '17CCE3FB-4883-4338-BB25-0D7996F9DD48', '上海分公司')
        return HttpResponse(returnValue)

