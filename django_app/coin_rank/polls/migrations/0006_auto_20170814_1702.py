# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-14 17:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_auto_20170814_0654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='price_change',
            name='price_change',
            field=models.FloatField(),
        ),
    ]
