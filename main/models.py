# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
# Create your models here.

class sys_logs(models.Model):
	id = models.AutoField(primary_key=True)
	username = models.CharField(max_length = 30)
	time = models.DateTimeField(auto_now_add=True)
	action = models.CharField(max_length=500)
	result = models.CharField(max_length=100)

class mail_info(models.Model):
	mail_host = models.CharField(max_length = 50 )
	mail_port = models.CharField(max_length = 4 )
	mail_user = models.CharField(max_length = 20 )
	mail_pass = models.CharField(max_length = 50 )
	mail_postfix = models.CharField(max_length = 50 )
	to_list = models.CharField(max_length = 200)

