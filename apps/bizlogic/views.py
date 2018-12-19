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
from django.views.decorators.csrf import csrf_protect
from apps.bizlogic.service.base.UserService import UserSerivce
from apps.bizlogic.service.base.OrganizeService import OrganizeService
from apps.bizlogic.service.base.StaffService import StaffService
from apps.bizlogic.models import Piorganize
from apps.bizlogic.models import Pistaff
from apps.bizlogic.models import Pistafforganize


# Create your views here.

class PiuserTest(View):
    def get(self, request):
        staff = Pistaff()
        staff.id = uuid.uuid1()
        staff.isdimission = 0
        staff.deletemark = 0
        staff.enabled = 1
        staff.gender = '男'
        staff.realname = '张三'
        staff.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        staff.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        returnCode, returnMessage, returnValue = StaffService.Add(self, staff)
        staffId = staff.id

        staff1 = Pistaff()
        staff1.id = uuid.uuid1()
        staff1.isdimission = 0
        staff1.deletemark = 0
        staff1.enabled = 1
        staff1.gender = '男'
        staff1.realname = '张三'
        staff1.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        staff1.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        returnCode, returnMessage, returnValue = StaffService.Add(self, staff1)

        starffOrg = Pistafforganize()
        starffOrg.id = uuid.uuid1()
        starffOrg.deletemark = 0
        starffOrg.enabled = 1
        starffOrg.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        starffOrg.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        starffOrg.staffid = staffId
        starffOrg.organizeid = '07B501A9-697A-4226-816D-003903FC8AA5'
        starffOrg.save()
        print(len(Pistaff.objects.all()))
        print(len(Pistafforganize.objects.all()))
        return HttpResponse(returnValue)

