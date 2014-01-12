#Create your views here
# -*- coding: utf-8 -*- 
import string
import re
from collections import defaultdict #for tf
import csv
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


def KeyCombinationQuantification(file_name, attr_names, regex):
	test_feature_date = defaultdict(int)
	time_record = []
	date_featurescore = 'date,freq\n'
	f = open(file_name,'r')

	for row in csv.DictReader(f):
		time = row['發佈時間'].split(' ')
		for attr in attr_names:
			if re.search(regex,row[attr]):
				print row['發佈時間']
				print attr
				print row[attr]
				time = row['發佈時間'].split(' ')
				test_feature_date[time[0]] += 1
				time_record.append(time[0])		
					
		
	time_record = list(set(time_record))
	time_record.sort()
	for time in time_record:
		date_featurescore += time + ',' + str(test_feature_date[time]) +'\n'

	

	Feature1_table = open('Feature1_table.csv','w')
	Feature1_table.write(date_featurescore)

	f.close()


KeyCombinationQuantification('Opview.csv', ['標題','內容'], "牛排|薯條|缺點|陳秉文")

