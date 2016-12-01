# -*- coding: utf-8 -*-
import os,sys
import salt.client
client = salt.client.LocalClient()
#caller = salt.client.Caller()
#local = caller.sminion.functions['grains.items'] 
#remote = client.cmd('QZ-DLZ-Test-001','grains.item',['os','osrelease','virtual','manufacturer' ])
#remote2 = client.cmd('Sina-EVA-S1','grains.item',['os','osrelease','virtual','manufacturer' ])
'''
grains_list = ['server_id','host','ipv4','mem_total','cpu_model','os']
for host_list in os.listdir('/etc/salt/pki/master/minions'):
	info = client.cmd(host_list,'grains.item',grains_list)
	#print info
	for key in info.values():
		print type(key)
		print key['host']
'''

#print remote
#print remote2
for host_list in os.listdir('/etc/salt/pki/master/minions'):
	print host_list

