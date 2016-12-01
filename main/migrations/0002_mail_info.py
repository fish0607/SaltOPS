# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-10-20 13:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='mail_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mail_host', models.CharField(max_length=50)),
                ('mail_port', models.CharField(max_length=4)),
                ('mail_user', models.CharField(max_length=20)),
                ('mail_pass', models.CharField(max_length=50)),
                ('mail_postfix', models.CharField(max_length=50)),
                ('to_list', models.CharField(max_length=200)),
            ],
        ),
    ]
