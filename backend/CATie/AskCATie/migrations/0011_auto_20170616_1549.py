# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-16 15:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AskCATie', '0010_auto_20170616_1114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='AskCATie.Question', verbose_name='Question'),
        ),
    ]
