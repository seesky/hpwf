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

        returnValue = RoleService.GetRoleUserIds(self, '1ecaa1f5-22d4-43ca-96e2-26c50ab43b75')
        return HttpResponse(returnValue)

