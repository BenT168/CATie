# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-15 11:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AskARi', '0002_auto_20170615_1059'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='parent',
            new_name='parent',
        ),
        migrations.AlterUniqueTogether(
            name='comment',
            unique_together=set([('parent', 'id_per_parent')]),
        ),
    ]
