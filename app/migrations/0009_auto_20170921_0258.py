# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-21 02:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20170921_0254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkin',
            name='leaveTime',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
