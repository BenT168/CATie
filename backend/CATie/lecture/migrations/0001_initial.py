# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-01-09 11:59
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('login', '0001_initial'),
        ('courses', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('urlName', models.CharField(default='', editable=False, max_length=60, validators=[django.core.validators.RegexValidator('^[a-zA-Z0-9]*$', "Only alphanumeric characters and '-' are allowed.")])),
                ('video', models.URLField(blank=True)),
                ('slides', models.URLField(blank=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Course')),
            ],
        ),
        migrations.CreateModel(
            name='UserNotes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.TextField()),
                ('lecture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lecture.Lecture')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.CATieProfile')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='lecture',
            unique_together=set([('urlName', 'course')]),
        ),
    ]