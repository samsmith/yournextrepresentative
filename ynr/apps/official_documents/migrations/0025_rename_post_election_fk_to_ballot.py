# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-07-16 13:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("official_documents", "0024_add_relevant_pages")]

    operations = [
        migrations.RenameField(
            model_name="officialdocument",
            old_name="post_election",
            new_name="ballot",
        )
    ]