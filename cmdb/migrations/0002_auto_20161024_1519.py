# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-10-24 15:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='host_info',
            old_name='flag_id',
            new_name='server_id',
        ),
    ]
