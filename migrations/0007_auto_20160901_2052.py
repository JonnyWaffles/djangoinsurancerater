# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-09-01 20:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('djangoinsurancerater', '0006_auto_20160901_2029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='insuringagreement',
            name='agreement_type',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='djangoinsurancerater.AgreementType'),
        ),
    ]