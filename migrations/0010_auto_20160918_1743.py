# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-09-18 17:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangoinsurancerater', '0009_auto_20160917_1528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='insuringagreement',
            name='id',
            field=models.PositiveIntegerField(primary_key=True, serialize=False),
        ),
    ]
