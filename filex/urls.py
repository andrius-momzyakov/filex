"""fexchanger URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from exchapp import views as ex
import ureg.views
import ureg.urls
import tracreg.urls

urlpatterns = [
    url(r'^$', ex.startpage, name='start'),
    url(r'^tracreg/', include(tracreg.urls)),
    url(r'^(?P<reg_slug>\w+)/', include(ureg.urls)),
    url(r'^home/$', ex.home, name='home'),
    url(r'^delete/(?P<doc_id>[0-9]+)/$', ex.delete, name='delete'),
    url('^accounts/', include('django.contrib.auth.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^private/(?P<name>.*)$', ex.serve_file, name='file'),

]