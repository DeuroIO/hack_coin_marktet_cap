# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-20 03:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_auto_20170814_1702'),
    ]

    operations = [
        migrations.AddField(
            model_name='coin',
            name='coin_image',
            field=models.ImageField(default=django.utils.timezone.now, upload_to=''),
            preserve_default=False,
        ),
    ]
