#!/usr/bin/env python
# -*- coding:utf-8 -*-

import csv
from main import file_to_id
from get_bill_csv import get_csv

#total_renew = [['eip-31ow4tev', 'uhost-xsqpkckk'],['eip-ipb245', 'uhost-suqi0jzs']]

#csv_file = 'order-detail-50140109-2019-08.csv'
mem_csv = []
bill_array = []
all_cost = []

def csv_to_mem(): #将csv文件转换成内存里的二维数组。
	with open(get_csv(),'r',encoding='UTF-8') as f:
		f_csv =csv.reader(f)
		for row in f_csv:
			mem_csv.append(row)


def get_singleIdCost(resource_id):  #从账单查出该id所有当月账单，并将消费价格存入到数组里。
	#print(len(mem_csv))
	bill_array.clear()
	for i in range(len(mem_csv)):
		if resource_id in mem_csv[i][4]:
			bill_array.append(float(mem_csv[i][20]))
			#print(resource_id)
	#print(bill_array)
	totalCost = sum(bill_array)
	print('The id %s cost %.2f ' %(resource_id,totalCost))
	return totalCost

	


def sum_allIdCost():
	csv_to_mem()
	total_renew = file_to_id()
	for i in range(len(total_renew)):
		count = 0
		for j in range(len(total_renew[i])):
			old = count
			count = get_singleIdCost(total_renew[i][j])
			count = old + count
		print('This TOTAL id_group cost %.2f' %count)

if __name__=='__main__':
	sum_allIdCost()