# -*- coding: utf-8 -*-
from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
import datetime
import sys,json

from main.views import save_log

reload(sys)
sys.setdefaultencoding('utf8')

def index(request):
	return render(request,'auth/login.html')

@csrf_exempt
def account_login(request):
	if request.method == "POST":
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = auth.authenticate(username=username,password=password)
		if user and user.is_active:
			auth.login(request,user)
			save_log(username,"登陆系统","登陆成功")
			return HttpResponseRedirect('/main/home/')
		else:
			return render(request,'auth/login.html',{'login_err': '登陆失败,请确认后重新输入'})
	else:
		return render(request,'auth/login.html')

def account_logout(request):
	save_log(request.user,"退出系统","成功")
	auth.logout(request)
	return render(request,"auth/login.html")

@login_required()
def profile(request):
	return render(request,"auth/profile.html",locals())

@login_required()
def help(request):
	return render(request,"help.html",locals())

@login_required()
def change_pass(request):
	username = request.GET.get('save')
	username = request.POST.get('user')
	password = request.POST.get('old_pass')
	new_pass1 = request.POST.get('new_pass1')
	new_pass2 = request.POST.get('new_pass2')
	if username:
		if new_pass1 == new_pass2:
			user = auth.authenticate(username=username,password=password)
			if user and user.is_active:
				newuser = User.objects.get(username=username)
				newuser.set_password(new_pass1)
				try:
					newuser.save()
					save_log(request.user,"修改密码","修改成功")
					return render(request,'auth/login.html')
				except Exception,e:
					log = "修改失败！！！"
					save_log(request.user,"修改密码","修改失败")
					return render(request,"auth/account_conf.html",locals())
			else:
				log = "请输入正确的密码！！！"
				return render(request,"auth/account_conf.html",locals())
		else:				
			log = "两次输入的密码不一致"
			return render(request,"auth/account_conf.html",locals())
	else:
		log = "修改成功将会要求重新登陆！！！"
		return render(request,"auth/account_conf.html",locals())

