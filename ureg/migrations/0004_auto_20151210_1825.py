# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('ureg', '0003_auto_20151112_1727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='regverificationkey',
            name='creation_date',
            field=models.DateTimeField(verbose_name='Создано', blank=True, default=datetime.datetime(2015, 12, 10, 18, 25, 52, 466205), null=True),
        ),
    ]
