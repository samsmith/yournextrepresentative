# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-04-06 14:55


from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('official_documents', '0020_add_post_election_values'),
    ]

    operations = [
        migrations.AlterField(
            model_name='officialdocument',
            name='post_election',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='candidates.PostExtraElection'),
        ),
    ]
