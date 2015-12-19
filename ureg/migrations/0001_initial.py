# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RegVerificationKey',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('key', models.CharField(verbose_name='GUID', max_length=40)),
                ('creation_date', models.DateTimeField(verbose_name='Создано')),
                ('activation_date', models.DateTimeField(verbose_name='Активировано')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
    ]
