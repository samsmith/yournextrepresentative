# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-04-24 18:26


from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uk_results', '0035_auto_20180406_1555'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='councilelection',
            name='controller_resultset',
        ),
        migrations.RemoveField(
            model_name='councilelection',
            name='council',
        ),
        migrations.RemoveField(
            model_name='councilelection',
            name='election',
        ),
        migrations.RemoveField(
            model_name='councilelection',
            name='party_set',
        ),
        migrations.RemoveField(
            model_name='councilelectionresultset',
            name='controller',
        ),
        migrations.RemoveField(
            model_name='councilelectionresultset',
            name='council_election',
        ),
        migrations.RemoveField(
            model_name='councilelectionresultset',
            name='reviewed_by',
        ),
        migrations.RemoveField(
            model_name='electionarea',
            name='election',
        ),
        migrations.RemoveField(
            model_name='electionarea',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='electionarea',
            name='winning_party',
        ),
        migrations.RemoveField(
            model_name='partywithcolour',
            name='party',
        ),
        migrations.DeleteModel(
            name='Council',
        ),
        migrations.DeleteModel(
            name='CouncilElection',
        ),
        migrations.DeleteModel(
            name='CouncilElectionResultSet',
        ),
        migrations.DeleteModel(
            name='ElectionArea',
        ),
        migrations.DeleteModel(
            name='PartyWithColour',
        ),
    ]
