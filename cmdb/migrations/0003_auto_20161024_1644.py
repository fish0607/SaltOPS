# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-10-24 16:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0002_auto_20161024_1519'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='host_info',
            name='disk',
        ),
        migrations.RemoveField(
            model_name='host_info',
            name='group',
        ),
        migrations.RemoveField(
            model_name='host_info',
            name='notes',
        ),
        migrations.RemoveField(
            model_name='host_info',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='host_info',
            name='position',
        ),
        migrations.RemoveField(
            model_name='host_info',
            name='salt_status',
        ),
    ]
