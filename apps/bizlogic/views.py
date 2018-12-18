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
        returnValue = OrganizeService.GetChildrensIdByCode(self, '01')
        return HttpResponse(returnValue)

