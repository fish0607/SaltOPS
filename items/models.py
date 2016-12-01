# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class items_info(models.Model):
	items_id = models.AutoField(max_length=50,primary_key=True,verbose_name='应用ID')
	hostname =  models.CharField(max_length=100,blank=True,verbose_name='计算机全称')
	server_id = models.CharField(max_length=50,blank=True,verbose_name='目标ID')
	item_name = models.CharField(max_length=100,blank=True,verbose_name='应用全称')
	service = models.CharField(max_length=100,blank=True,verbose_name='应用全称')
	updata = models.CharField(max_length=100,blank=True,verbose_name='updata_shell')
	version_bak = models.CharField(max_length=100,blank=True,verbose_name='备份版本')
	version_run = models.CharField(max_length=100,blank=True,verbose_name='版本')
	version_new = models.CharField(max_length=100,blank=True,verbose_name='更新版本')
	port = models.CharField(max_length=50,null=True,verbose_name='item_port')
	status = models.CharField(max_length=100,null=True,verbose_name='item_status')
	group = models.CharField(max_length=100,null=True,verbose_name='item_group')
	notes = models.CharField(max_length=100,null=True,verbose_name='item_notes')

