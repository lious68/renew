#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import json
import time
import datetime
import configparser
import urllib.request
from ucloud.core import exc
from ucloud.client import Client


#读取配置
config = configparser.ConfigParser()
config.read('config.ini',encoding='"utf-8-sig')
public_key = config.get("key","public_key")
private_key = config.get("key","private_key")
project_id = config.get("key","project_id")
region = config.get("key","region")
year = int(config.get("check_account","year"))
month = int(config.get("check_account","month"))

#读取日期，并转换成时间戳
make_date = datetime.datetime(year,month,10)
timestamp = time.mktime(make_date.timetuple())

#构造请求
client = Client({
    "region": region,
    "project_id": project_id,
    "public_key" : public_key,
    "private_key" : private_key
})





def initial_request():
	d = {"BillPeriod":timestamp,"BillType":"1","PaidType":"1"}
	try:
		resp = client.invoke("GetBillDataFileUrl",d)
	except exc.RetCodeException as e:
		resp = e
	#print(json.dumps(resp, sort_keys=True, indent=4, separators=(',', ': ')))
	#print(resp.get('FileUrl'))
	return resp
def eip():
	try:
		resp = client.invoke("DescribeEIP")
	except exc.RetCodeException as e:
		resp = e
	#return resp
	print(resp)

def get_csv():
	currt_path = os.getcwd()
	dowloadurl = initial_request().get('FileUrl')
	file = urllib.request.urlretrieve(dowloadurl)
	return file[0]



if __name__=='__main__':
	initial_request()