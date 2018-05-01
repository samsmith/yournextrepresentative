# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-04-06 14:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uk_results', '0034_auto_20180130_1243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='councilelectionresultset',
            name='review_status',
            field=models.CharField(blank=True, choices=[(None, 'Unreviewed'), ('unconfirmed', 'Unconfirmed'), ('confirmed', 'Confirmed'), ('rejected', 'Rejected')], max_length=100),
        ),
        migrations.AlterField(
            model_name='resultset',
            name='review_status',
            field=models.CharField(blank=True, choices=[(None, 'Unreviewed'), ('unconfirmed', 'Unconfirmed'), ('confirmed', 'Confirmed'), ('rejected', 'Rejected')], max_length=100),
        ),
    ]
