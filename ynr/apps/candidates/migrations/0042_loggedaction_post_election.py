# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-05-01 16:37


from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('candidates', '0041_auto_20180323_1400'),
    ]

    operations = [
        migrations.AddField(
            model_name='loggedaction',
            name='post_election',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='candidates.PostExtraElection'),
        ),
    ]
