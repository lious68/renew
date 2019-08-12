#!/usr/bin/env python
# -*- coding:utf-8 -*-

from ucloud.core import exc
from ucloud.client import Client
import urllib.request
import time
import os
import json
import configparser

config = configparser.ConfigParser()
config.read('config.ini',encoding='UTF-8')
public_key = config.get("key","public_key")
private_key = config.get("key","private_key")
project_id = config.get("key","project_id")
region = config.get("key","region")


client = Client({
    "region": region,
    "project_id": project_id,
    "public_key" : public_key,
    "private_key" : private_key
})



timestamp = time.time()

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