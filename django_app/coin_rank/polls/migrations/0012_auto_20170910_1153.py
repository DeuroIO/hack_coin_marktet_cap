# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-10 11:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0011_auto_20170910_0108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tokentransaction',
            name='timestamp',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.TimeStamp'),
        ),
    ]
