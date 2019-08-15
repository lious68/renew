#!/usr/bin/env python
# -*- coding:utf-8 -*-
import logging
import json
import os
import configparser

from ucloud.core import exc
from ucloud.client import Client


# with open("config.ini",'r',encoding="utf-8") as f:
# 	content = f.read()
# 	content = re.sub(r"\xfe\xff","",content)
# 	content = re.sub(r"\xff\xfe","",content)
# 	content = re.sub(r"\xef\xbb\xbf", "", content)
#

#设置logger
logger = logging.getLogger('ucloud')
logger.disabled = True




total_renew = [] #需要续费的总清单
id_array = []  #每个eip关联的eipid，uhostid和磁盘id
switch_arry = [] #用于转换的中间列表

#读取配置
config = configparser.ConfigParser()
config.read('config.ini',encoding='"utf-8-sig')
public_key = config.get("key","public_key")
private_key = config.get("key","private_key")
project_id = config.get("key","project_id")
region = config.get("key","region")
renew_status = config.get("renew","renew_status")

#构造client字典
client = Client({
	"region": region,
	"project_id": project_id,
	"public_key" : public_key,
	"private_key" : private_key
})


def initial_request():
	try:
		resp = client.invoke("DescribeEIP")
	except exc.RetCodeException as e:
		resp = e
	return resp


def get_eipid(eip): #获得该项目的所有EIP，遍历找到输入的eip
	eipSets = initial_request().get('EIPSet')
	for eipSet in eipSets:
		ip = eipSet.get('EIPAddr')[0].get('IP')
		if ip == eip: #如果找到输入的IP，则记下eipid和uhostid
			eip_id = eipSet.get('EIPId')
			uhost_id = eipSet.get('Resource').get('ResourceID')
			id_array.append(eip_id)
			id_array.append(uhost_id)
			return  uhost_id


def get_diskid(uhost_id):
	d = {"UHostIds":[uhost_id]} #构造请求字典
	try:
		resp = client.uhost().describe_uhost_instance(d)
	except exc.UCloudException as e:
		print(e)
	else:
		for i in range(len(resp['UHostSet'][0]['DiskSet'])):
			if i < 1:
				#print('just only system disk')
				pass
			else:
				disk_id = resp['UHostSet'][0]['DiskSet'][i]['DiskId']
				id_array.append(disk_id)
		switch_arry = id_array.copy()
		total_renew.append(switch_arry)
		id_array.clear()

def create_renew(resource_id):
	d = {"ResourceId": resource_id, "ChargeType": "Month", "Quantity": "1"} #构造续费接口参数。默认按1个月续费
	try:
		resp = client.invoke("CreateRenew", d)
	except exc.RetCodeException as e:
		resp = e
	else:
		print("thest ids %s has been renewed" % total_renew)


def file_to_id(dir):
	file = os.path.join(dir,'eip.txt')
	with open(file,'r') as f:
		for line in f.readlines():
			get_diskid(get_eipid(line.strip()))
	return total_renew

def main():
	#从同目录下的文件eip.txt里取出eip，按行读取后，找出关联的eipid，uhostid，diskid
	currt_dir = os.path.abspath(os.path.dirname(__file__))
	file_to_id(currt_dir)
	#把每个id取出来，并续费。
	for list in total_renew:
		for resourceId in list:
			if renew_status == 'ON':
				create_renew(resourceId)
	print("These  %s ID will be renew,is right?" %total_renew)


if __name__=='__main__':
	main()