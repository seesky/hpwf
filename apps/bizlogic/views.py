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
from apps.bizlogic.service.base.UserService import UserSerivce


# Create your views here.

class PiuserTest(View):
    def get(self, request):
        roleIds = ['674CD840-F480-454F-ABD8-D8CD2CAB73912']
        # idsTrue = ['17CCE3FB-4883-4338-BB25-0D7996F9DD48']
        # ids = ['0009ed41-3753-4f99-b52d-4ea6a43dda1a','0003d3f5-6aa1-4475-adf6-50961c8bd739']
        # # #userPage = UserSerivce.GetDTByPage(self, '', '07DF66FA-644E-4B1F-9994-AE7332796058', '27A40BF7-D68C-4BF5-9B40-056A8D3E9A81', 2, None)
        #userList = UserSerivce.Search(self, '', '', roleIds)
        #userList = UserSerivce.SetUserAuditStates(self, ids, None)

        # returnValue = Piuserrole.objects.filter(userid='674CD840-F480-454F-ABD8-D8CD2CAB731A').delete()
        # returnValue = Pipermission.objects.filter(Q(resourcecategory=Piuser._meta.db_table) & Q(resourceid='674CD840-F480-454F-ABD8-D8CD2CAB731A')).delete()
        # returnValue = Pipermissionscope.objects.filter(Q(resourcecategory=Piuser._meta.db_table) & Q(resourceid='674CD840-F480-454F-ABD8-D8CD2CAB7391')).delete()
        #returnValue = UserSerivce.BatchDelete(self, roleIds)
        returnValue = UserSerivce.GetDepartmentUsers(self, 'f2a1d304-3436-4387-872e-a9dbe39108cd', False)
        for u in returnValue:
            print(u.get('ID'))
        return HttpResponse(returnValue)

