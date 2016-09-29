# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-06 17:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wunderlist', '0013_auto_20160706_1955'),
    ]

    operations = [
        migrations.AddField(
            model_name='connection',
            name='habit_title',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Habit Title'),
        ),
        migrations.AlterField(
            model_name='connection',
            name='habit_id',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Habit ID'),
        ),
    ]