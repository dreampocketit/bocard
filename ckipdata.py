#Create your views here
# -*- coding: utf-8 -*-
import random
import simplejson
import Orange
from ckip import CKIPSegmenter, CKIPParser
import urllib2
import json
import string
import re
import time
from collections import defaultdict #for tf
import csv
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import os, sys, urllib, json
import urllib2
from dateutil import parser
from operator import itemgetter
import matplotlib.pyplot as plt
import numpy as np
from pylab import *
import sqlite3

TrashWord = ['氣炸','鍋','我','有','是','來','為','你','他','這樣','說']

def CkipCrawlerData(file_name):
	f = open(file_name,'r')
	data = 'PostId,CkipDataContent\n'
	term_frequency= defaultdict( int )
	PostId=0
	for row in csv.DictReader(f):
		ckip_json = CkipReturn(row['內容'])
		CkipDataContent =''
		for sentence in ckip_json['result']:
			for term in sentence:
				if term['pos']=='N' or term['pos'] == 'Vi' or term['pos'] == 'Vt':
					CkipDataContent += '-'+term['term']
					if str(term['term']) not in TrashWord:
						term_frequency[term['term']]+=1
		data+=str(PostId)+','+CkipDataContent+'\n'
		print data
		PostId+=1

	
        CkipCrawlerDataTable = open('CkipCrawlerDataTable.csv','w')
        CkipCrawlerDataTable.write(data)
        CkipCrawlerDataTable.close()

        filtered_term_table = open('FilteredTermTable.txt','w')
        for key in term_frequency:
		if key not in TrashWord:
			if term_frequency[key]>5:
                		filtered_term_table.write(str(key)+':'+str(term_frequency[key])+'\n')
	filtered_term_table.close()
	

def CkipReturn(in_text): #in_text is string
	segmenter = CKIPSegmenter('changcheng.tu', 'a10206606')
	try:
		segmented_in_text_result = segmenter.process(unicode(in_text))
	except:
		segmented_in_text_result = segmenter.process(unicode('got an error'))
	return segmented_in_text_result

def CreateTable(term_table,data_table):
	feature_set = [] #for possible bursty feature which total frequency is more than 2
	f = open(term_table,'r') #termset
	df = open(data_table,'r')
	term_post_table = open('TermPostTable.csv','w')
	term_post_table.seek(0)
	data = 'PostId'
	for row in f:
		term = row.split(':')
		feature_set.append(term[0])
	for feature in feature_set:
		data+=','+feature
	data+='\n'
	for row in csv.DictReader(df):
		num=0
		token = row['CkipDataContent'].split('-')
		feature_dict = defaultdict(int)
		for feature in feature_set:
			feature_dict[feature]+=0
		for word in token:
			feature_dict[word]+=1

		row_data = str(row['PostId'])
		for feature in feature_set:
			num=num+1
			if feature_dict[feature]==0:
				row_data+=','+'0'
			else:
				row_data+=','+'1'
		data+=row_data+'\n'
	f.close()
	df.close()
	term_post_table.write(str(data))
	term_post_table.close()

CkipCrawlerData('Opview.csv')
CreateTable('FilteredTermTable.txt','CkipCrawlerDataTable.csv')
