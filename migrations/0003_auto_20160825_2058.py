# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-08-25 20:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangoinsurancerater', '0002_auto_20160823_1456'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='accountinfo',
            options={'verbose_name': 'Account'},
        ),
        migrations.AddField(
            model_name='insuringagreement',
            name='premium',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=11, null=True, verbose_name='Agreement Premium'),
        ),
        migrations.AlterField(
            model_name='accountinfo',
            name='name',
            field=models.CharField(max_length=30, verbose_name="Insured's Name"),
        ),
        migrations.AlterField(
            model_name='quote',
            name='underwriter',
            field=models.CharField(max_length=30, verbose_name="Underwriter's name"),
        ),
    ]
