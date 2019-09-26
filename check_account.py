#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import csv
from renew import file_to_id
from get_bill_csv import get_csv


mem_csv = []
bill_array = []
all_cost = []
id_cost = []

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
	singleCost = sum(bill_array)
	id_cost.append(resource_id)
	id_cost.append(singleCost)
	print(id_cost)
	print('The id %s cost %.2f ' %(resource_id,singleCost))
	return singleCost

	


def sum_allIdCost():
	csv_to_mem()
	currt_dir = os.path.abspath(os.path.dirname(__file__))
	total_renew = file_to_id(currt_dir)
	for i in range(len(total_renew)):
		count = 0
		for j in range(len(total_renew[i])):
			old = count
			count = get_singleIdCost(total_renew[i][j])
			count = old + count
		print('This group cost %.2f' %count)

if __name__=='__main__':
	sum_allIdCost()