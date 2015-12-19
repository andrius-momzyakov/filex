__author__ = 'amomzyakov'

from django.conf.urls import include, url
from django.contrib import admin
from exchapp import views as ex
from ureg import views as reg

urlpatterns = [
    url(r'^register/$', reg.reg, name='reg'),
    url(r'^done/$', reg.done, kwargs={'title':'Пользователь создан.', 'body':'Пользователь создан. \
                                    Перейдите в почту, откройте уведомление и перейдите по ссылке \
                                    для подтверждения.'}, name='done'),
    url(r'^verified/$', reg.done, kwargs={'title':'Учетная запись активирована.', 'body':'Теперь Вы можете войти \
                                под своей учетной записью.'}, name='verified'),
    url(r'^verification_failed/$', reg.done, kwargs={'title':'Ошибка при подтверждении учетной записи.', 'body':'При \
                                подтверждении учетной записи произошла ошибка.'}, name='verifiсation_failed'),
    url(r'^verify/([a-zA-Z0-9\-]{1,40})', reg.verify, name='verify'),
]

