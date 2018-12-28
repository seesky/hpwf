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

from apps.bizlogic.service.base.LogOnService import LogOnService




# Create your views here.

class PiuserTest(View):
    def get(self, request):

        statusCode,returnValue = LogOnService.UserLogOn(self, 'gx', '1234567', '', False)
        return HttpResponse(statusCode)

