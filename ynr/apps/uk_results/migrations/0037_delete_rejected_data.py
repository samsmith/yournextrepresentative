# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-04-24 18:44
from __future__ import unicode_literals

from django.db import migrations

def delete_rejected_results(apps, schema_editor):
    ResultSet = apps.get_model("uk_results", "ResultSet")
    ResultSet.objects.filter(review_status='rejected').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('uk_results', '0036_auto_20180424_1926'),
    ]

    operations = [
        migrations.RunPython(
            delete_rejected_results, migrations.RunPython.noop,
        )
    ]
