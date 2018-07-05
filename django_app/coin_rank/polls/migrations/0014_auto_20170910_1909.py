# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-10 19:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0013_auto_20170910_1221'),
    ]

    operations = [
        migrations.AddField(
            model_name='coin',
            name='largested_timestamp',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='polls.TimeStamp'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='coin',
            name='number_of_timestamps',
            field=models.FloatField(default=0),
        ),
    ]