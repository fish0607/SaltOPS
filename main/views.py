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

from main.models import *
from cmdb.models import *
from salt_api import *

reload(sys)
sys.setdefaultencoding('utf8')

#setting upload dir
upload_dir = os.path.join(sys.path[0],"upload")

@login_required()
def home(request):
	net_sent = '{0:.2f} Mb'.format(psutil.net_io_counters().bytes_recv / 1024 / 1024)
	net_rcvd = '{0:.2f} Mb'.format(psutil.net_io_counters().bytes_sent / 1024 / 1024)
	cpu = psutil.cpu_times()
	men = psutil.virtual_memory()
	disk = psutil.disk_partitions()
	sys_user = psutil.users()
	#print cpu,men,disk,sys_user
	if os.system("/etc/init.d/salt-master status >/dev/null") != 0:
		master_status = "Salt Master 未运行!!!"
	else:
		master_status = "Salt Master 运行中..."
	return render(request,'index.html',locals())

@login_required()
def salt_master(request):
	while os.system("/etc/init.d/salt-master status >/dev/null") != 0:
		#master_status = "salt-master 未运行。"
		#time.sleep(5)
		os.system('/etc/init.d/salt-master start')
		time.sleep(5)
	master_stauts = os.popen('/etc/init.d/salt-master status').read()	

	Accepted_Keys = os.listdir('/etc/salt/pki/master/minions')
	Denied_Keys = os.listdir('/etc/salt/pki/master/minions_denied')
	Unaccepted_Keys = os.listdir('/etc/salt/pki/master/minions_pre')
	Rejected_Keys = os.listdir('/etc/salt/pki/master/minions_rejected')
	Accepted_count = Denied_conut = Unaccepted_count = Rejected_count = 0
	for i in os.walk('/etc/salt/pki/master/minions'):
		Accepted_count += 1
	for i in os.walk('/etc/salt/pki/master/minions_denieds'):
		Denied_conut += 1
	for i in os.walk('/etc/salt/pki/master/minions_pre'):
		Unaccepted_count += 1
	for i in os.walk('/etc/salt/pki/master/minions_rejected'):
		Rejected_count += 1
	
	return render(request,'salt/salt_master.html',locals())

@login_required()
def salt_minion(request):
	import salt.client
	client = salt.client.LocalClient()
	Accepted_Keys = os.listdir('/etc/salt/pki/master/minions')
	minion_count = 0 
	for i in Accepted_Keys:
		minion_count += 1
	minion_list = client.cmd('*','test.ping',[])
	print minion_list
	return render(request,'salt/salt_minion.html',locals())

@login_required()
def salt_shell(request):
	host_list = os.listdir('/etc/salt/pki/master/minions')
	get_host_list = request.POST.getlist('name_id')
	cmd = request.POST.get('command')
	if get_host_list is not None and cmd is not None:
		import salt.client
		client = salt.client.LocalClient()
		result = []
		for host in get_host_list:
			try:
				result.append(client.cmd(host,'cmd.run',[cmd]))
			except Exception,e:
				result.append(e)
				return render(request,'salt/salt_shell.html',locals())
		print result
		return render(request,'salt/salt_shell.html',locals())
	else:
		log = "请选择要执行命令的主机并输入命令。"
		return render(request,'salt/salt_shell.html',locals())
	
@login_required()
def filelist(request):
	file_list = os.listdir(upload_dir)
	return render(request,'files/files_info.html',locals())

@login_required
def files_del(request):
	del_list = request.POST.getlist('del')
	if del_list is not None:
		for name in del_list:
			del_file = os.path.join(upload_dir, name)	
			if os.path.isfile(del_file):
				try:
					os.remove(del_file)
					save_log(request.user,"删除文件：" + name,"删除成功")
					return HttpResponseRedirect('/file/info/')
				except Exception,e:
					save_log(request.user,"删除文件：" + name,e) 
					return HttpResponseRedirect('/main/log/')
			elif os.path.isdir(del_file):
				try:
					#os.removedirs(del_file)
					import shutil
					shutil.rmtree(del_file)
					save_log(request.user,"删除目录：" + name,"删除成功")
					return HttpResponseRedirect('/file/info/')
				except Exception,e:
					save_log(request.user,"删除目录：" + name,e)
					return HttpResponseRedirect('/main/log/')
			else:
				return HttpResponseRedirect('/file/info/')
	else:
		return HttpResponseRedirect('/file/info/')

@login_required()
def files_upload(request):
	from django import forms 
	class UploadFileForm(forms.Form): 
		title = forms.CharField(max_length=65536) 
		file = forms.FileField() 
	if request.method == "GET": 
		#data='get'
		print request.GET
		return HttpResponseRedirect('/file/info/')
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
			return HttpResponseRedirect('/file/info/')
	return HttpResponseRedirect('/file/info/')

@login_required()
def files_download(request):
	file_list = os.listdir(upload_dir)
	down_list = request.POST.get('download')
	if down_list:
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

@login_required()
def conf_mail(request):
	mail_conf = mail_info.objects.all()
	
	save = request.GET.get('save')
	edit = request.GET.get('edit')
	remove = request.GET.get('remove')
	send = request.GET.get('send')

	mail_host = request.POST.get('mail_host')
	mail_port = request.POST.get('mail_port')
	mail_user = request.POST.get('mail_user')
	mail_pass = request.POST.get('mail_pass')
	mail_postfix = request.POST.get('mail_postfix')
	to_list = request.POST.get('to_list')
	if save:
		sql = mail_info(id=save,mail_host=mail_host,mail_port=mail_port,mail_user=mail_user,mail_pass=mail_pass,mail_postfix=mail_postfix,to_list=to_list)
		try:
			sql.save()
			save_log(request.user,"Mail config","ok")
			return HttpResponseRedirect('/main/mail/')
		except Exception,e:
			save_log(request.user,"Mail config",e)	
	elif edit:
		mail_conf = mail_info.objects.get(id=edit)
		return render(request,'main/mail_edit.html',locals())
	elif remove:
		del_sql = mail_info.objects.filter(id=remove)
		del_sql.delete()
		save_log(request.user,"remove mail conf","ok")
		return HttpResponseRedirect('/main/mail/')
	elif send:
		res = send_mail("测试","此邮件为测试发送~~")
		return render(request,'main/system_mail.html',locals())	
	elif not mail_conf:
		return render(request,'main/mail_conf.html',locals())
	else:
		return render(request,'main/mail_info.html',locals())

@login_required()
def show_log(request):
	log_list = sys_logs.objects.order_by("-id")
	return render(request,'main/show_log.html',locals())

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

def save_log(username,action,result):
	sql_info = sys_logs(username=username,action=action,result=result)
	try:
		sql_info.save()
	except Exception,e:
		return e

def send_mail(subject,context):
	import smtplib
	import os,sys
	from email.mime.text import MIMEText
	from email.header import Header
	mail_conf = mail_info.objects.get(id=1)

	msg = MIMEText(context,'plain','utf-8')
	msg['From'] = Header("Auto OPS")
	msg['To'] = ";".join((mail_conf.to_list).split(";"))
	msg['Subject'] = Header(subject, 'utf-8')
	
	send_smtp = smtplib.SMTP()
	send_smtp.connect(mail_conf.mail_host, int(mail_conf.mail_port))
	send_smtp.login(mail_conf.mail_user, mail_conf.mail_pass)
	try:
		for list in (mail_conf.to_list).split(";"):
			send_smtp.sendmail(mail_conf.mail_user, list, msg.as_string())
		send_smtp.close()
		return True
	except Exception, e:
		print str(e)
		return False

def salt_cmd(host,cmd):
	import salt.client
	client = salt.client.LocalClient()
	res = client.cmd('*','cmd.run',['ls'])
	print res
	return res

def salt_run_shell(host,shell):
	import salt.client
	
