# -*- coding: utf-8 -*-
# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
import time,datetime
import os,sys
import json
import psutil

from main.views import save_log
from cmdb.models import *

reload(sys)
sys.setdefaultencoding('utf8')

#setting upload dir
upload_dir = os.path.join(sys.path[0],"upload")
download_dir = os.path.join(sys.path[0],"download")

@login_required()
def files_info(request):
	file_list = os.listdir(upload_dir)
	return render(request,'files/files_info.html',locals())

@login_required
def files_remove(request):
	del_list = request.POST.getlist('del')
	if del_list is not None:
		for name in del_list:
			del_file = os.path.join(upload_dir, name)	
			if os.path.isfile(del_file):
				try:
					os.remove(del_file)
					save_log(request.user,"删除文件：" + name,"删除成功")
					return HttpResponseRedirect('/files/info/')
				except Exception,e:
					save_log(request.user,"删除文件：" + name,e) 
					return HttpResponseRedirect('/main/log/')
			elif os.path.isdir(del_file):
				try:
					#os.removedirs(del_file)
					import shutil
					shutil.rmtree(del_file)
					save_log(request.user,"删除目录：" + name,"删除成功")
					return HttpResponseRedirect('/files/info/')
				except Exception,e:
					save_log(request.user,"删除目录：" + name,e)
					return HttpResponseRedirect('/main/log/')
			else:
				return HttpResponseRedirect('/files/info/')
	else:
		return HttpResponseRedirect('/files/info/')

@login_required()
def files_upload(request):
	from django import forms 
	class UploadFileForm(forms.Form): 
		title = forms.CharField(max_length=65536) 
		file = forms.FileField() 
	if request.method == "GET": 
		#data='get'
		print request.GET
		return HttpResponseRedirect('/files/info/')
	if request.method == "POST":
		if (request.FILES['t_file']):
			try:
				f = save_upload_file(request.FILES['t_file']) 
				save_log(request.user,'上传文件:' + f.name,'上传成功')
				file_list = os.listdir(upload_dir)
				return render(request,'files/files_info.html',locals())
			except Exception,e:
				save_log(request.user,'上传文件',e)
				return HttpResponseRedirect('/mian/log/')
		else:
			return HttpResponseRedirect('/files/info/')
	return HttpResponseRedirect('/files/info/')

@login_required()
def files_download(request):
	file_list = os.listdir(upload_dir)
	down_list = request.POST.get('download')
	if down_list:
		from django.http import StreamingHttpResponse
		response = StreamingHttpResponse(file_iterator(down_list))
		response['Content-Type'] = 'application/octet-stream'
		response['Content-Disposition'] = 'attachment;filename="{0}"'.format(down_list)
		#return response
		return render(request,'files/files_download.html',locals())
	else:
		return render(request,'files/files_download.html',locals())


@login_required()
def files_rsync(request):
	file_list = os.listdir(upload_dir)
	host_list = host_info.objects.all()
	return render(request,'files/files_rsync.html',locals())

def save_upload_file(f):
	f_path = os.path.join(upload_dir, f.name)
	with open(f_path, 'wb+') as info: 
		#print f.name 
		for chunk in f.chunks(): 
			info.write(chunk) 
	return f 

def file_iterator(file_name, chunk_size=512):
	with open(file_name) as f:
		while True:
			c = f.read(chunk_size)
			if c:
				yield c
			else:
				break

