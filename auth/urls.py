# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.contrib import admin
from auth import views

urlpatterns = [
	url(r'^login/$',views.account_login,name='login'),
	url(r'^logout/$',views.account_logout,name='logout'),
	url(r'^set/$',views.change_pass,name='changepass'),
	url(r'^profile/$',views.profile,name='profile'),
]
