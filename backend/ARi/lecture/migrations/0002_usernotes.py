# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-18 15:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_auto_20170613_1543'),
        ('lecture', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserNotes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.TextField()),
                ('lecture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lecture.Lecture')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.ARiProfile')),
            ],
        ),
    ]