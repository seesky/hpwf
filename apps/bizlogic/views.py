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
from apps.bizlogic.service.base.PermissionItemService import PermissionItemService
from apps.bizlogic.service.base.ModuleService import ModuleService
from apps.bizlogic.models import Piorganize
from apps.bizlogic.models import Pistaff
from apps.bizlogic.models import Pistafforganize
from apps.bizlogic.models import Piuser
from apps.bizlogic.models import Pirole


# Create your views here.

class PiuserTest(View):
    def get(self, request):
        #returnValue = ModuleService.GetDT(self)
        #ids = ['cd29da80-c330-419f-acca-bc6df878fce2', '37255D5C-EA7E-49F2-9B66-18D7C8151B79', '0AC690ED-8935-438C-A7BE-3245061F0566']
        #returnValue = ModuleService.GetDTByIds(self, ids)
        #returnValue = ModuleService.GetFullNameByCode(self, 'frmKyqAjmlCx')
        returnValue = ModuleService.GetPermissionIds(self, '5909F64F-A5A3-4D8E-BAE9-942C76F596F8')
        return HttpResponse(returnValue)

