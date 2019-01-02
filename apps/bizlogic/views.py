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

from apps.bizlogic.service.permission.ScopPermission import ScopPermission




# Create your views here.

class PiuserTest(View):
    def get(self, request):

        returnValue = ScopPermission.GetUserDTByPermissionScope(self, '333FCB67-A69B-4821-98CC-CD8CDBF7FC2C', 'OrganizeManagement.Permission')
        return HttpResponse(returnValue)

