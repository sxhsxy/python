"""hello URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from . import views
import person.views
import django.contrib.auth.views
#import django.contrib.auth.urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.hello, name='hi'),
    url(r'^person/', person.views.index),
    url(r'^polls/', include('polls.urls')),
    url(r'^chaxun/', include('chaxun.urls')),
    url(r'^accounts/', include('users.urls')),
    #url(r'^accounts/login/', django.contrib.auth.views.LoginView.as_view())
]
