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

        returnValue = ScopPermission.GetUserDTByPermissionScope(self, '37FFB38A-720C-43E6-AD78-1DB055444DEB', 'DAGL.DAZL')
        return HttpResponse(returnValue)

