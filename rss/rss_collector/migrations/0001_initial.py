# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-23 22:17
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feeds',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('publish_time', models.DateTimeField(blank=True, default=datetime.datetime.now, null=True)),
                ('link', models.URLField(max_length=300)),
                ('author', models.TextField(max_length=200)),
                ('img_url', models.URLField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Sources',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('url', models.URLField()),
            ],
        ),
        migrations.AddField(
            model_name='feeds',
            name='source_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rss_collector.Sources'),
        ),
    ]
