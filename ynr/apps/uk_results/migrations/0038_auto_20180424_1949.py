# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-04-24 18:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uk_results', '0037_delete_rejected_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resultset',
            name='final_source',
        ),
        migrations.RemoveField(
            model_name='resultset',
            name='is_final',
        ),
    ]
