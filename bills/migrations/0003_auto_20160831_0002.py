# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-31 00:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0002_auto_20160515_2333'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='title',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='bill',
            name='title_without_number',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
