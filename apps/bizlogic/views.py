import datetime
from django.shortcuts import render
from django.views.generic.base import View
from .models import Piuser
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect

# Create your views here.

class PiuserTest(View):
    def get(self, request):
        user = Piuser.objects.get(id='0003d3f5-6aa1-4475-adf6-50961c8bd739')
        return HttpResponse(user.realname)
