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

from apps.bizlogic.service.permission.PermissionService import PermissionService




# Create your views here.

class PiuserTest(View):
    def get(self, request):

        returnCode = PermissionService.GetPermissionScopeByUserId(self, '26F43BC9-AE6D-42D2-BAC9-F4237A949484', 'UserAdmin')
        return HttpResponse(returnCode)

