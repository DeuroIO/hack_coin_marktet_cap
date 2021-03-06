# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-13 17:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coin_name', models.CharField(max_length=1024)),
                ('coin_symbol', models.CharField(max_length=1024)),
                ('sector', models.CharField(max_length=1024)),
                ('tech', models.CharField(max_length=1024)),
                ('star', models.IntegerField(default=-1)),
                ('investment_memo', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Historical',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('daily_timestamp', models.DateTimeField()),
                ('votes', models.IntegerField(default=0)),
                ('average_price', models.FloatField()),
                ('volume', models.FloatField()),
                ('circulating_cap', models.FloatField()),
                ('total_cap', models.FloatField()),
                ('coin_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Coin')),
            ],
        ),
        migrations.CreateModel(
            name='Price_Change',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('daily_timestamp', models.DateTimeField()),
                ('price_change', models.IntegerField()),
                ('coin_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Coin')),
            ],
        ),
        migrations.CreateModel(
            name='Rank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('daily_timestamp', models.DateTimeField()),
                ('rank', models.IntegerField()),
                ('coin_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Coin')),
            ],
        ),
    ]
