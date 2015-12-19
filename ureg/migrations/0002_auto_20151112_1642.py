# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('ureg', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='regverificationkey',
            name='activation_date',
            field=models.DateTimeField(verbose_name='Активировано', blank=True),
        ),
        migrations.AlterField(
            model_name='regverificationkey',
            name='creation_date',
            field=models.DateTimeField(verbose_name='Создано', default=datetime.datetime(2015, 11, 12, 16, 42, 32, 467217), blank=True),
        ),
    ]
