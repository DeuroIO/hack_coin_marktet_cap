# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-12 11:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0015_auto_20170912_1123'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='account_memo',
            field=models.TextField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]