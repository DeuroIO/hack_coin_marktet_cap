# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-14 06:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_auto_20170814_0616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historical',
            name='daily_timestamp',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.TimeStamp'),
        ),
        migrations.AlterField(
            model_name='price_change',
            name='daily_timestamp',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.TimeStamp'),
        ),
        migrations.AlterField(
            model_name='rank',
            name='daily_timestamp',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.TimeStamp'),
        ),
    ]