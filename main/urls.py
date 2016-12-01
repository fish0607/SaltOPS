from django.conf.urls import include, url
from django.contrib import admin
from main import views

urlpatterns = [
	url(r'^home/$',views.home,name='home'),
	url(r'^log/$',views.show_log,name='log'),
	url(r'^mail/$',views.conf_mail,name='conf_mail'),
	url(r'^master/$',views.salt_master,name='salt_master'),
	url(r'^minion/$',views.salt_minion,name='salt_minion'),
	url(r'^shell/$',views.salt_shell,name='salt_shell'),
]

