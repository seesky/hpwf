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


# Create your views here.

class PiuserTest(View):
    def get(self, request):
        returnValue = StaffService.GetDTByOrganize(self, '07B501A9-697A-4226-816D-003903FC8AA5', False)
        return HttpResponse(returnValue)

