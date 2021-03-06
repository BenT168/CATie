# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-01-09 11:59
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import re


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('lecture', '0001_initial'),
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionAndCurrentUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('relevant_comment_ids', models.TextField(validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:\\,\\d+)*\\Z', 32), code='invalid', message='Enter only digits separated by commas.')])),
            ],
            options={
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=4000)),
                ('score', models.IntegerField(default=0)),
                ('id_per_question', models.PositiveIntegerField(editable=False)),
                ('downvoters', models.ManyToManyField(editable=False, related_name='downvoted_set', to='login.CATieProfile')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('body', models.TextField(max_length=4000)),
                ('id_per_lecture', models.PositiveIntegerField(editable=False)),
                ('last_interaction', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lecture.Lecture')),
                ('poster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.CATieProfile')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AskCATie.Question', verbose_name='Question'),
        ),
        migrations.AddField(
            model_name='comment',
            name='parent_comment',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='AskCATie.Comment'),
        ),
        migrations.AddField(
            model_name='comment',
            name='poster',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='poster_set', to='login.CATieProfile'),
        ),
        migrations.AddField(
            model_name='comment',
            name='upvoters',
            field=models.ManyToManyField(editable=False, related_name='upvoted_set', to='login.CATieProfile'),
        ),
        migrations.AlterUniqueTogether(
            name='question',
            unique_together=set([('parent', 'id_per_lecture')]),
        ),
        migrations.AlterUniqueTogether(
            name='comment',
            unique_together=set([('parent', 'id_per_question')]),
        ),
    ]
