# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('ureg', '0002_auto_20151112_1642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='regverificationkey',
            name='activation_date',
            field=models.DateTimeField(verbose_name='Активировано', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='regverificationkey',
            name='creation_date',
            field=models.DateTimeField(verbose_name='Создано', null=True, default=datetime.datetime(2015, 11, 12, 17, 27, 29, 1870), blank=True),
        ),
    ]
