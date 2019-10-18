#!/usr/bin/env python
# -*- coding:utf-8 -*-
import logging
import json
import os
import csv
import configparser
import time
import datetime
import urllib.request
from ucloud.core import exc
from ucloud.client import Client

#设置logger
logger = logging.getLogger('ucloud')
logger.disabled = True

eip_array = [] #yuanshi eip
eip_region_array = []
mem_csv = []
bill_array = []
all_cost = []
id_cost = []
total_renew = [] #需要续费的总清单
bind_all = [] #eip和对应绑定ID信息
serialization = [["eip","placeholder","eipId","eipIdCost","uhostId","uhostIdCost"]] #存到csv文件的数据
id_array = []  #每个eip关联的eipid，uhostid和磁盘id
switch_cost = [] #用于转换的中间列表
regions = [ 'cn-bj2', 'cn-gd', 'cn-sh', 'cn-sh2', 'hk', 'cn-bj1','tw-kh', 'tw-tp','us-ws', 'us-ca',  'ge-fra', 'th-bkk', 'kr-seoul', 'sg',  'rus-mosc', 'jpn-tky', 'uae-dubai', 'idn-jakarta', 'ind-mumbai', 'bra-saopaulo', 'uk-london', 'afr-nigeria', 'vn-sng', 'cn-qz']

#读取配置
currt_dir = os.path.abspath(os.path.dirname(__file__))
cfgfile = os.path.join(currt_dir,'config.ini')
config = configparser.ConfigParser()
config.read(cfgfile,encoding='"utf-8-sig')
public_key = config.get("key","public_key")
private_key = config.get("key","private_key")
project_id = config.get("key","project_id")
region = config.get("key","region")
renew_status = config.get("renew","renew_status")
year = int(config.get("check_account","year"))
month = int(config.get("check_account","month"))
#读取日期，并转换成时间戳
make_date = datetime.datetime(year,month,10)
timestamp = time.mktime(make_date.timetuple())



def convert_id(dir):
	file = os.path.join(dir,'eip.txt')
	with open(file,'r') as f:
		for line in f.readlines():
			eip_array.append(line.strip())


def ip_related_region():
	for region in regions:
		region_attemp = region
		#构造client字典
		client = Client({
			"region": region_attemp,
			"project_id": project_id,
			"public_key" : public_key,
			"private_key" : private_key
		})
		try:
			resp = client.invoke("DescribeEIP")
		except exc.RetCodeException as e:
			resp = e
		eipset1 = resp.get('EIPSet')
		if eipset1:
			eipset2 = eipset1[0].get('EIPAddr')
			for i in range(len(eipset1)):
				for j in range(len(eipset2)):
					eip_get = eipset1[i].get('EIPAddr')[j].get("IP")
					if eip_get in eip_array:
						#print([eip_get,region_attemp])
						eip_region_array.append([eip_get,region_attemp])


#eip_region_array =[['117.50.82.95', 'cn-bj2'], ['106.75.5.77', 'cn-bj2'], ['106.75.167.49', 'cn-gd'], ['103.98.17.48', 'tw-tp'], ['107.150.100.182', 'us-ca']]

def find_eip_uhost_id(eip,rzone): #获得该项目的所有EIP，遍历找到输入的eip
	client = Client({
		"region": rzone,
		"project_id": project_id,
		"public_key" : public_key,
		"private_key" : private_key
	})
	try:
		resp = client.invoke("DescribeEIP")
	except exc.RetCodeException as e:
		resp = e
	eipSets = resp.get('EIPSet')
	for eipSet in eipSets:
		ip = eipSet.get('EIPAddr')[0].get('IP')
		if ip == eip: #如果找到输入的IP，则记下eipid和uhostid
			eip_id = eipSet.get('EIPId')
			uhost_id = eipSet.get('Resource').get('ResourceID')
			id_array.append(eip)
			id_array.append(eip_id)
			id_array.append(uhost_id)
			#return  uhost_id

			d = {"UHostIds": [uhost_id]}  # 构造请求字典
			try:
				resp = client.uhost().describe_uhost_instance(d)
			except exc.UCloudException as e:
				print(e)
			else:
				for i in range(len(resp['UHostSet'][0]['DiskSet'])):
					if i < 1:
						# print('just only system disk')
						pass
					else:
						disk_id = resp['UHostSet'][0]['DiskSet'][i]['DiskId']
						id_array.append(disk_id)
				switch_arry = id_array.copy()
				# bind_all.extend(id_array)
				# switch_serial = bind_all.copy()
				# serialization.append(switch_serial)
				total_renew.append(switch_arry)
				#print(total_renew)
				id_array.clear()



def initial_bill_request():
	client = Client({
		"region": 'cn-bj2',
		"project_id": project_id,
		"public_key" : public_key,
		"private_key" : private_key
	})
	d = {"BillPeriod":timestamp,"BillType":"1","PaidType":"1"}
	try:
		resp = client.invoke("GetBillDataFileUrl",d)
	except exc.RetCodeException as e:
		resp = e
	return resp


def get_csvFile():
	currt_path = os.getcwd()
	dowloadurl = initial_bill_request().get('FileUrl')
	file = urllib.request.urlretrieve(dowloadurl)
	return file[0]


def csv_to_mem():  # 将csv文件转换成内存里的二维数组。
	with open(get_csvFile(), 'r', encoding='UTF-8') as f:
		f_csv = csv.reader(f)
		for row in f_csv:
			mem_csv.append(row)


def get_singleIdCost(resource_id):  # 从账单查出该id所有当月账单，并将消费价格存入到数组里。
	# print(len(mem_csv))
	bill_array.clear()
	for i in range(len(mem_csv)):
		if resource_id in mem_csv[i][4]:
			bill_array.append(float(mem_csv[i][20]))
	singleCost = sum(bill_array)
	id_cost.append(resource_id)
	id_cost.append(singleCost)
	print('The id %s cost %.2f ' % (resource_id, singleCost))
	return singleCost


def sum_allIdCost():
	csv_to_mem()
	currt_dir = os.path.abspath(os.path.dirname(__file__))
	convert_id(currt_dir)
	print(total_renew)
	for i in range(len(total_renew)):
		count = 0
		for j in range(len(total_renew[i])):
			old = count
			count = get_singleIdCost(total_renew[i][j])
			count = old + count
		id_cost.append(count)
		switch_cost = id_cost.copy()
		serialization.append(switch_cost)
		id_cost.clear()
		print('This group cost %.2f' % count)
	#print(serialization)

def wite_csv():
	with open("checkAccount.csv", "w") as csvfile:
		writer = csv.writer(csvfile)
		# 先写入columns_name
		#writer.writerow(["index", "a_name", "b_name"])
		writer.writerows(serialization)

def main():
	convert_id(os.path.dirname(__file__))
	ip_related_region()
	#print(eip_region_array)
	for i in range(len(eip_region_array)):
		ee = eip_region_array[i]
		find_eip_uhost_id(ee[0], ee[1])
	sum_allIdCost()
	wite_csv()

if __name__=='__main__':
	main()