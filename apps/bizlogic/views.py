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

from bizlogic.service.base.RoleService import RoleService




# Create your views here.

class PiuserTest(View):
    def get(self, request):
        #returnValue = ModuleService.GetDT(self)
        #ids = ['cd29da80-c330-419f-acca-bc6df878fce2', '37255D5C-EA7E-49F2-9B66-18D7C8151B79', '0AC690ED-8935-438C-A7BE-3245061F0566']
        #returnValue = ModuleService.GetDTByIds(self, ids)
        #returnValue = ModuleService.GetFullNameByCode(self, 'frmKyqAjmlCx')
        returnValue = RoleService.GetDTByOrganize(self, '122D09C4-72C1-4371-846F-3D778080822C', True)
        return HttpResponse(returnValue)

