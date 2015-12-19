from datetime import datetime

from django.db import models

from django.contrib.auth.models import User

# Create your models here.

class RegVerificationKey(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь')
    key = models.CharField(verbose_name='GUID', max_length=40)
    creation_date = models.DateTimeField(default=datetime.now(), verbose_name='Создано', null=True, blank=True)
    activation_date = models.DateTimeField(verbose_name='Активировано', null=True, blank=True)