# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.contrib import admin
from items import views

urlpatterns = [
	url(r'^info/$',views.items_info_echo,name='items_info'),
	url(r'^add/$',views.items_add,name='items_add'),
	url(r'^action/$',views.items_action,name='items_action'),
	url(r'^version/$',views.items_version,name='items_version'),
	url(r'^log/$',views.items_log,name='items_log'),
	url(r'^monitor/$',views.items_monitor,name='items_monitor'),
]
