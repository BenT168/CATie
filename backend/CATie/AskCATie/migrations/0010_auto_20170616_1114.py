# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-16 11:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AskCATie', '0009_auto_20170616_1107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='downvoted',
            field=models.ManyToManyField(editable=False, related_name='downvoted_set', to='login.CATieProfile'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AskCATie.Question', verbose_name='Question'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='upvoted',
            field=models.ManyToManyField(editable=False, related_name='upvoted_set', to='login.CATieProfile'),
        ),
    ]
