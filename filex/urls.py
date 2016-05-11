"""taskman URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from taskman.exchapp import views as ex

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', ex.startpage, name='start'),
    url(r'^home/$', ex.home, name='home'),
    url(r'^delete/(?P<doc_id>[0-9]+)/$', ex.delete, name='delete'),
#    url('^accounts/login', auth_views.login),
#    url('^accounts/logout', auth_views.logout),
#    url('^accounts/password_change', auth_views.password_change),
    url(r'^private/(?P<name>.*)$', ex.serve_file, name='file'),
    url('^accounts/', include('django.contrib.auth.urls')),
]
