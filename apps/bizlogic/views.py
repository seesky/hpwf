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
from apps.bizlogic.models import Piorganize
from apps.bizlogic.models import Pistaff
from apps.bizlogic.models import Pistafforganize
from apps.bizlogic.models import Piuser
from apps.bizlogic.models import Pirole


# Create your views here.

class PiuserTest(View):
    def get(self, request):
        # userId = '26F43BC9-AE6D-42D2-BAC9-F4237A949484'
        # q1 = Piuser.objects.filter(Q(id=userId) & Q(deletemark=0) & Q(enabled=1))
        # q2 = Piuserrole.objects.filter(
        #     Q(userid=userId) & Q(roleid__in=Pirole.objects.filter(deletemark=0).values('id')) & Q(
        #         deletemark=0)).values_list('roleid', flat=True)
        # returnValue = q1.union(q2)

        #returnValue = PermissionItemService.GetLicensedDT(self, "333FCB67-A69B-4821-98CC-CD8CDBF7FC2C", 'OrganizeManagement.Permission')
        returnValue = PermissionItemService.GetIdsByModule(self, "8895495B-F4A8-4EDD-8401-4ADAA0F9A67A")
        return HttpResponse(returnValue)

