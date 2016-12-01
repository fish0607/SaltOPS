# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.contrib import admin
from cmdb import views

urlpatterns = [
	url(r'^info/$',views.cmdb_info,name='cmdb_info'),
    url(r'^ssh/$',views.cmdb_ssh,name='cmdb_ssh'),
]
