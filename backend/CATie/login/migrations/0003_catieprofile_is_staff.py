# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-01-08 17:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_auto_20170613_1543'),
    ]

    operations = [
        migrations.AddField(
            model_name='catieprofile',
            name='is_staff',
            field=models.BooleanField(default=True),
        ),
    ]
