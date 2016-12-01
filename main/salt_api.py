# -*- coding: utf-8 -*-
import os,sys
import salt.client
import salt.config
import salt.loader
import salt.key

def salt_master_status():
	while os.system("/etc/init.d/salt-master status >/dev/null") != 0:
		#master_status = "salt-master 未运行。"
		#time.sleep(5)
		os.system('/etc/init.d/salt-master start')
		time.sleep(5)
	master_stauts = os.popen('/etc/init.d/salt-master status').read()
	#key_list
	Accepted_Keys = os.listdir('/etc/salt/pki/master/minions')
	Denied_Keys = os.listdir('/etc/salt/pki/master/minions_denied')
	Unaccepted_Keys = os.listdir('/etc/salt/pki/master/minions_pre')
	Rejected_Keys = os.listdir('/etc/salt/pki/master/minions_rejected')
	
	return master_stauts,Accepted_Keys,Denied_Keys,Unaccepted_Keys,Rejected_Keys

def salt_minion_status():
	client = salt.client.LocalClient()
	Accepted_Keys = os.listdir('/etc/salt/pki/master/minions')
	minion_count = 0
	for i in os.walk('/etc/salt/pki/master/minions'):
		minion_count += 1
	for i in Accepted_Keys:
		minion_list = client.cmd(i,'test.ping',[])
	return minion_count,minion_list

def salt_shell(host,cmd):
	client = salt.client.LocalClient()
	res = client.cmd(host,'cmd.run',[cmd])
	return res

def transfe_file(host,src_file,dsc_file):
	client = salt.client.LocalClient()
	res = client.cmd(host,'cp.get_file',src_file,dsc_file)
	return res

def salt_grains():
	import salt.client
	caller = salt.client.Caller()
	caller.sminion.functions['grains.items']

def salt_key_list():
	client = salt.client.LocalClient()
	key_manager = salt.key.Key(client.opts)
	#key_manager.accept('QZ-MySQL-001')
	list = key_manager.list_keys()
	for key in list.items():
		#print type(key)
		#print key
		for i in key:
			#print type(i)
			print i 
salt_key_list()

