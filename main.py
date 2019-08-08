#!/usr/bin/env python
# -*- coding:utf-8 -*-

from ucloud.core import exc
from ucloud.client import Client
from config import *
import json


client = Client({
    "region": region,
    "project_id": project_id,
    "public_key" : public_key,
    "private_key" : private_key
})



total_renew = [] #需要续费的总清单
id_array = []  #每个eip关联的eipid，uhostid和磁盘id
switch_arry = [] #用于转换的中间列表

def initial_request():
	try:
		resp = client.invoke("DescribeEIP")
	except exc.RetCodeException as e:
		resp = e.json()
	return resp
	#获得该项目的所有EIP，遍历找到输入的eip

def get_eipid(eip):
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
		#print(json.dumps(resp,sort_keys=True, indent=4, separators=(',', ': ')))

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
	d = {"ResourceId": resource_id_id, "ChargeType": "Month", "Quantity": "1"} #构造续费接口参数。默认按1个月续费
	try:
		resp = client.invoke("CreateRenew", d)
	except exc.RetCodeException as e:
		resp = e.json()
	else:
		print(json.dumps(resp, sort_keys=True, indent=4, separators=(',', ': ')))

def file_to_id():
	with open('eip.txt','r') as f:
		for line in f.readlines():
			get_diskid(get_eipid(line.strip()))
	return total_renew

def main():
	#从同目录下的文件eip.txt里取出eip，按行读取后，找出关联的eipid，uhostid，diskid
	file_to_id()
	print(total_renew)

	#把每个id取出来，并续费。
	for list in total_renew:
		for resourceId in list:
			if renew == 'YES':
				create_renew(resourceId)
			else:
				print(resourceId)

if __name__=='__main__':
	main()