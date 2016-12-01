# -*- coding: utf-8 -*-
# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
import os,sys

from items.models import *
from cmdb.models import host_info
from main.views import save_log

reload(sys)
sys.setdefaultencoding('utf8')

@login_required()
def items_info_echo(request):
	items_list = items_info.objects.all()
	edit_id = request.GET.get('edit')
	save_id = request.GET.get('save')
	start_id = request.GET.get('start')
	stop_id = request.GET.get('stop')
	restart_id = request.GET.get('restart')
	update_id = request.GET.get('update')
	remove_id = request.GET.get('remove')
	if edit_id:
		items = items_info.objects.get(items_id=edit_id)
		return render(request,"items/items_change.html",locals())
	elif save_id:
		info = items_info.objects.get(items_id=save_id)	
		info.item_name = request.POST.get('item_name')
		info.service = request.POST.get('service')
		info.updata = request.POST.get('updata')
		info.port = request.POST.get('port')
		info.status = request.POST.get('status')
		info.group = request.POST.get('group')
		info.notes = request.POST.get('notes')
		try:
			info.save()
			save_log(request.user,"修改应用信息：" + info.item_name ,"修改成功")
			return HttpResponseRedirect('/items/info/')
		except Exception,e:
			log = "应用信息修改失败"
			save_log(request.user,"修改应用信息：" + info.item_name ,"修改失败")
			return render(request,"items/items_info.html",locals())
	elif remove_id:
		print remove_id
		del_info = items_info.objects.filter(items_id=remove_id)
		del_info.delete()
		return HttpResponseRedirect('/items/info/')	
	else:
		return render(request,"items/items_info.html",locals())

@login_required()
def items_action(request):
	items_list = items_info.objects.all()
	start_id = request.GET.get('start')
	stop_id = request.GET.get('stop')
	restart_id = request.GET.get('restart')
	updata_id = request.GET.get('updata')
	if start_id:
		info = items_info.objects.get(items_id=start_id)
		log = 'start' + str(info.item_name)
		action = info.service + 'start'
		res = salt_cmd(info.hostname,action)
		return render(request,"items/items_action.html",locals())
	elif stop_id:
		info = items_info.objects.get(items_id=stop_id)
		log = 'stop' + str(info.item_name)
		action = info.service + 'stop'
		res = salt_cmd(info.hostname,action)
		return render(request,"items/items_action.html",locals())
	elif restart_id:
		info = items_info.objects.get(items_id=restart_id)
		log = 'restart' + str(info.item_name)
		action = info.service + 'restart'
		res = salt_cmd(info.hostname,action)
		return render(request,"items/items_action.html",locals())
	elif updata_id:
		info = items_info.objects.get(items_id=updata_id)
		log = 'update' + str(info.item_name)
		action = info.updata + 'updata'
		res = salt_cmd(info.hostname,action)
		return render(request,"items/items_action.html",locals())
	else:
		return render(request,"items/items_action.html",locals())

@login_required()
def items_add(request):
	server_list = host_info.objects.all()

	server_id = request.POST.get('server_id')
	hostname = request.POST.get('hostname')
	item_name = request.POST.get('item_name')
	service = request.POST.get('service')
	updata = request.POST.get('updata')
	port = request.POST.get('port')
	status = request.POST.get('status')
	group = request.POST.get('group')
	notes = request.POST.get('notes')

	if hostname is not None:
		if len(item_name):
			if len(service):
				print hostname,item_name,service
				info = items_info(hostname=hostname,item_name=item_name,service=service,updata=updata,port=port,status=status,group=group,notes=notes)
				try:
					info.save()
					save_log(request.user,"添加应用信息：" + info.item_name ,"添加成功")
					return HttpResponseRedirect('/items/info/')
				except Exception,log:
					#log = '应用信息添加失败'
					save_log(request.user,"添加应用信息失败",log)
					return render(request,"items/items_add.html",locals())
			else:
				log = '应用信息不完整，请填充完整'
				return render(request,"items/items_add.html",locals())
		else:
			log = '应用信息不完整，请填充完整'
			return render(request,"items/items_add.html",locals())
	else:
		log = '应用信息不完整，请填充完整'
		return render(request,"items/items_add.html",locals())

@login_required()
def items_version(request):
	items_list = items_info.objects.all()
	return render(request,"items/items_version.html",locals())
@login_required()	
def items_monitor(request):
	return render(request,"items/items_monitor.html",locals())

@login_required() 
def items_log(request):
	return render(request,"items/items_logs.html",locals())

def salt_cmd(host,action)
	import salt.client
	client = salt.client.LocalClient()
	try:
		res = client.cmd(host,'cmd.run',action)
	except Exception,res:
		return res
	return res

