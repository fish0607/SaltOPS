from django.conf.urls import include, url
from django.contrib import admin
from files import views

urlpatterns = [
	url(r'^info/$',views.files_info,name='files_info'),
	url(r'^remove/$',views.files_remove,name='files_del'),
	url(r'^upload/$',views.files_upload,name='files_upload'),
	url(r'^download/$',views.files_download,name='files_download'),
	url(r'^rsync/$',views.files_rsync,name='files_rsync'),
]

