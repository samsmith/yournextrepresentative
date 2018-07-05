# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-05-18 10:40


from django.db import migrations


def add_extra_fields_to_base(apps, schema_editor):
    Membership = apps.get_model('popolo', 'Membership')

    # First, delete any Membership objects with no extra
    Membership.objects.filter(extra=None).delete()

    for base in Membership.objects.all().select_related('extra'):
        base.elected = base.extra.elected
        base.party_list_position = base.extra.party_list_position
        base.post_election = base.extra.post_election
        base.save()


class Migration(migrations.Migration):

    dependencies = [
        ('popolo', '0003_move-extra-fields-to-base'),
    ]

    operations = [
        migrations.RunPython(add_extra_fields_to_base,
                             migrations.RunPython.noop),
    ]
