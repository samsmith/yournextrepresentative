# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-04-24 20:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uk_results', '0044_auto_20180424_2149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resultset',
            name='ip_address',
            field=models.GenericIPAddressField(null=True),
        ),
    ]
