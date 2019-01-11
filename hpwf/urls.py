"""hpwf URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from apps.bizlogic.views import PiuserTest
from django.conf.urls import url, include
app_name = '[hadmin]'

urlpatterns = [
    url(r'^piusertest/$', PiuserTest.as_view(), name='piusertest'),
    url(r'^Admin/', include(('hadmin.urls', 'hadmin'), namespace='hadmin'))
]
