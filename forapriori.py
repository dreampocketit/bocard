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

TrashWord = []
f_trash = open('TrashWordsFile.txt','r')
for row in f_trash:
	TrashWord.append(re.sub(r"\n", "", row ))

def CkipCrawlerData(file_name):
	f = open(file_name,'r')
	data = 'PostId,CkipDataContent\n'
	term_frequency= defaultdict( int )
	PostId=0
	for row in csv.DictReader(f):
		ckip_json = CkipReturn(row['內容'])
		CkipDataContent = ''
		for sentence in ckip_json['result']:
			for term in sentence:
				if term['pos']=='N' or term['pos'] == 'Vi' or term['pos'] == 'Vt':
					CkipDataContent += '-'+term['term']
					if term['term'] not in TrashWord:
						term_frequency[term['term']]+=1
		
					else:
						print term['term']
		data+=str(PostId)+','+CkipDataContent+'\n'
		PostId+=1

	
        CkipCrawlerDataTable = open('CkipCrawlerDataTable.csv','w')
        CkipCrawlerDataTable.write(data)
        CkipCrawlerDataTable.close()

        filtered_term_table = open('FilteredTermTable.txt','w')
        for key in term_frequency:
		if key not in TrashWord:
			if term_frequency[key]>7:
                		filtered_term_table.write(str(key)+':'+str(term_frequency[key])+'\n')
	filtered_term_table.close()
	

def CkipReturn(in_text): #in_text is string
	segmenter = CKIPSegmenter('changcheng.tu', 'a10206606')
	try:
		segmented_in_text_result = segmenter.process(unicode(in_text))
	except:
		segmented_in_text_result = segmenter.process(unicode('got an error'))
	return segmented_in_text_result

def CreateBasket(term_table,data_table):
	feature_set = [] #for possible bursty feature which total frequency is more than 2
	syn_dict = Synonym('synonym.txt')
	f = open(term_table,'r') #termset
	df = open(data_table,'r')
	term_post_table = open('TermPost.basket','w')
	data = 'PostId'
	for row in f:
		term = row.split(':')
		if term[0] in syn_dict:
			if syn_dict[term[0]] not in feature_set:
				feature_set.append(syn_dict[term[0]])
		else:
			feature_set.append(term[0])
	data=''
	for row in csv.DictReader(df):
		print  row['CkipDataContent']
		token = row['CkipDataContent'].split('-')
		for word in token:
			if word in syn_dict:
				data+=','+syn_dict[word]
			else:
				if word in feature_set:
					data+=','+word	
		data+='\n'
	f.close()
	df.close()
	term_post_table.write(str(data))
	term_post_table.close()


def Synonym(f_name):
	f = open('synonym.txt','r')
	syn_dict = defaultdict(str)
	for row in f:
		print row
		syn = row.split(':')
		syn_dict[syn[0]]=syn[1]

	return syn_dict

CkipCrawlerData('Opview.csv')
#CreateTable('FilteredTermTable.txt','CkipCrawlerDataTable.csv')
CreateBasket('FilteredTermTable.txt','CkipCrawlerDataTable.csv')
#Synonym('test')
