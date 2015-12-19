# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('exchapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='readers',
            field=models.ManyToManyField(verbose_name='Читатели (для непубличного доступа)', to=settings.AUTH_USER_MODEL, null=True, related_name='reader', blank=True),
        ),
    ]
