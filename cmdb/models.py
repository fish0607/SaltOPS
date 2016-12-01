# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

# Create your models here.
class host_info(models.Model):
	server_id = models.CharField(primary_key=True,max_length=50,blank=True,verbose_name='目标ID')
	hostname = models.CharField(max_length=100,blank=True,verbose_name='计算机全称')
	ip = models.CharField(max_length=500,blank=True,verbose_name='IP')
	cpu = models.CharField(max_length=100,blank=True,verbose_name='CPU型号')
	men = models.CharField(max_length=10,blank=True,verbose_name='内存')
	disk = models.CharField(max_length=10,blank=True,verbose_name='硬盘')
	os = models.CharField(max_length=50,blank=True,verbose_name='操作系统')
	position = models.CharField(max_length=100,blank=True)
	owner = models.CharField(max_length=100,blank=True)
	group = models.CharField(max_length=100,blank=True,verbose_name='所属组')
	salt_status  = models.BooleanField(default=False,verbose_name='Salt状态')
	notes = models.CharField(max_length=100,blank=True,verbose_name='备注')

class ssh_info(models.Model):
	server_id = models.CharField(primary_key=True,max_length=50,blank=True,verbose_name='目标ID')
	hostname = models.CharField(max_length=100,blank=True,verbose_name='计算机全称')
	ip = models.CharField(max_length=500,blank=True,verbose_name='IP')
	username = models.CharField(max_length=50,blank=True,verbose_name='用户名')
	password = models.CharField(max_length=100,blank=True,verbose_name='密码')
	port = models.CharField(max_length=10,blank=True,verbose_name='Port')
	notes = models.CharField(max_length=100,blank=True,verbose_name='备注')

