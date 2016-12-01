# -*- coding: utf-8 -*-
# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import datetime
import os,sys
import json
import string

from cmdb.models import host_info,ssh_info
from main.views import save_log

reload(sys)
sys.setdefaultencoding('utf8')

@login_required()
def cmdb_info(request):
	server_list = host_info.objects.all()
	change = request.GET.get('change')
	remove = request.GET.get('remove')
	save = request.GET.get('save')
	refresh = request.GET.get('refresh')

	if change:
		info = host_info.objects.get(server_id=change)
		return render(request,'cmdb/host_change.html',locals())
	elif save:
		ip = request.GET.get('save')
		info = host_info.objects.get(server_id=save)
		info.hostname = request.POST.get('hostname')
		info.cpu = request.POST.get('cpu')
		info.men = request.POST.get('men')
		info.disk = request.POST.get('disk')
		info.os = request.POST.get('os')
		info.position = request.POST.get('position')
		info.owner = request.POST.get('owner')
		info.group = request.POST.get('group')
		info.notes = request.POST.get('notes')
		try:
			info.save()
			print info.ip,'aaaa'
			save_log(request.user,"修改主机信息：" + info.hostname ,"修改成功")
			return HttpResponseRedirect('/cmdb/info/')
		except Exception,log:
			#log = 'Host info save fail...'
			save_log(request.user,"修改主机信息：" + info.hostname ,log)
			return render(request,'cmdb/host_change.html',locals())	
	elif remove:
		del_host = host_info.objects.filter(server_id=remove)
		del_ssh = ssh_info.objects.filter(server_id=remove)
		del_host.delete()
		del_ssh.delete()
		save_log(request.user,"删除主机信息：" + remove ,"删除成功")
		return HttpResponseRedirect('/cmdb/info/')
	elif refresh:
		try:
			import salt.client
			client = salt.client.LocalClient()
			#client.cmd('*','saltutil.sync_grains',[])
			#client.cmd('*','grains.item',['virtual']) 是否虚拟机
			#client.cmd('*','grains.item',['manufacturer']) 制造商
			#client.cmd('*','grains.item',['num_cpus']) CPU核心数
			grains_list = ['server_id','host','ipv4','mem_total','cpu_model','cpuarch','os','oscodename','osrelease','osarch']
			for host_list in os.listdir('/etc/salt/pki/master/minions'):
				print 'refresh info:',host_list
				info = client.cmd(host_list,'grains.item',grains_list)
				for value in info.values():
					server_id = value['server_id']
					hostname = value['host']
					#ip = value['ipv4'][0]
					ip = value['ipv4']
					ip.remove('127.0.0.1')
					ip = ','.join(ip)
					cpu = str(value['cpu_model']) + ' ' + str(value['cpuarch'])
					men = value['mem_total']
					system = str(value['os']) + ' ' + str(value['oscodename']) + ' ' + str(value['osrelease']) + ' ' + str(value['osarch'])
				disk = client.cmd(host_list,'disk.usage',[])
				print disk
				for zone in disk.values():
					count = 0
					for size in zone.values():
						count = count + int(size['available'])
				disk = count / 1048576
				
				print server_id,hostname,ip,cpu,men,system,disk
				try:
					host_sql = host_info.objects.get(server_id=server_id)
					ssh_sql = ssh_info.objects.get(server_id=server_id)
					#if info is not None:
					print 'updata info',hostname
					host_sql.server_id = server_id
					host_sql.hostname = hostname
					host_sql.ip = ip
					host_sql.cpu = cpu
					host_sql.men = men
					host_sql.os = system
					host_sql.disk = disk
					host_sql.save()
					ssh_sql.server_id = server_id
					ssh_sql.hostname = hostname
					ssh_sql.ip = ip
					ssh_sql.save()
				except Exception,log:
					print 'add info',hostname
					sql_host = host_info(server_id=server_id,hostname=hostname,ip=ip,cpu=cpu,men=men,disk=disk,os=system)
					sql_ssh = ssh_info(server_id=server_id,hostname=hostname,ip=ip)
					sql_host.save()
					sql_ssh.save()
			return HttpResponseRedirect('/cmdb/info/')
		except Exception,log:
			print log
			return render(request,'cmdb/host_info.html',locals())
	else:
		return render(request,'cmdb/host_info.html',locals())

@login_required()
def cmdb_ssh(request):
	ssh_list = ssh_info.objects.all()
	change = request.GET.get('change')
	remove = request.GET.get('remove')
	save = request.GET.get('save')
	if change:
		info  = ssh_info.objects.get(server_id=change)
		return render(request,'cmdb/ssh_change.html',locals())
	elif save:
		ip = request.GET.get('save')
		info = ssh_info.objects.get(server_id=save)
		info.hostname = request.POST.get('hostname')
		info.ip = request.POST.get('ip')
		info.username = request.POST.get('username')
		info.password = request.POST.get('password')
		info.port = request.POST.get('port')
		info.notes = request.POST.get('notes')
		try:
			info.save()
			save_log(request.user,"修改主机SSH信息：" + save ,"修改成功")
			return HttpResponseRedirect('/cmdb/ssh/')
		except Exception,log:
			save_log(request.user,"修改主机SSH信息失败" + save ,log)
			return render(request,'cmdb/ssh_change.html',locals())
	elif remove:
		print remove
		del_host = host_info.objects.filter(server_id=remove)
		del_ssh = ssh_info.objects.filter(server_id=remove)
		del_host.delete()
		del_ssh.delete()
		save_log(request.user,"删除主机：" + remove ,"删除成功")
		return HttpResponseRedirect('/cmdb/ssh/')
	return render(request,'cmdb/ssh_info.html',locals())

