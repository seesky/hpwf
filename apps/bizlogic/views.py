import datetime
from django.shortcuts import render
from django.views.generic.base import View
from .models import Piuser
from .models import Piuserrole
from .models import Pipermission
from .models import Pipermissionscope
from django.db.models import Q


from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from apps.bizlogic.service.base.UserService import UserSerivce
from apps.bizlogic.service.base.OrganizeService import OrganizeService
from apps.bizlogic.models import Piorganize


# Create your views here.

class PiuserTest(View):
    def get(self, request):
        ids = ['07DF66FA-644E-4B1F-9994-AE7332796058', '07DF66FA-644E-4B1F-9994-AE7332796059']
        organzie = Piorganize()
        organzie.id = '07DF66FA-644E-4B1F-9994-AE7332796058';
        organzie.fullname = 'o1'
        organzie.isinnerorganize = 1
        organzie.deletemark = 0
        organzie.enabled = 1
        organzie.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        organzie.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        returnCode, returnMessage, returnValue = OrganizeService.Add(self, organzie)

        organzie1 = Piorganize()
        organzie1.id = '07DF66FA-644E-4B1F-9994-AE7332796059';
        organzie1.fullname = 'o1'
        organzie1.isinnerorganize = 1
        organzie1.deletemark = 0
        organzie1.enabled = 1
        organzie1.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        organzie1.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        returnCode1, returnMessage1, returnValue1 = OrganizeService.Add(self, organzie1)


        returndd = OrganizeService.BatchDelete(self, ids)

        return HttpResponse(returndd)

