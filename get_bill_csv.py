#!/usr/bin/env python
# -*- coding:utf-8 -*-

from ucloud.core import exc
from ucloud.client import Client
from config import *
import urllib.request
import time
import os
import json


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
		resp = e.json()
	#print(json.dumps(resp, sort_keys=True, indent=4, separators=(',', ': ')))
	#print(resp.get('FileUrl'))
	return resp

def get_csv():
	currt_path = os.getcwd()
	dowloadurl = initial_request().get('FileUrl')
	file = urllib.request.urlretrieve(dowloadurl)
	return file[0]



if __name__=='__main__':
	get_csv()