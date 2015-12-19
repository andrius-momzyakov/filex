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
            name='Document',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.FileField(max_length=255, verbose_name='Имя файла (до 255 букв) (*)', upload_to='')),
                ('duration', models.IntegerField(verbose_name='Сколько дней хранить (0-бессрочно) (*)', default=0)),
                ('comm', models.CharField(null=True, max_length=500, verbose_name='Комментарий к файлу', blank=True)),
                ('is_public', models.BooleanField(verbose_name='Публичный доступ', default=True)),
                ('author', models.ForeignKey(verbose_name='Кто загрузил (*)', to=settings.AUTH_USER_MODEL)),
                ('readers', models.ManyToManyField(related_name='reader', verbose_name='Читатели (для непубличного доступа)', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
