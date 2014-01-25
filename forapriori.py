#Create your views here
# -*- coding: utf-8 -*-
from ckip import CKIPSegmenter, CKIPParser
import string
from collections import defaultdict #for tf
import csv
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import os, sys, urllib, json
import urllib2
from dateutil import parser
import re

TERM_FREQ_THRESHOLE = 7
TRASH_WORD_FILE = 'TrashWordsFile.txt'
SYNONYM_FILE = 'synonym.txt'

def CkipCrawlerData(file_name):
	f = open(file_name,'r')
	data = 'CkipDataContent\n'
	term_frequency= defaultdict( int )

	for row in csv.DictReader(f):
		if row['來源']=='新聞':
			print 'this is news'+row['內容']
			continue
		ckip_json = CkipReturn(row['內容'])
		print 'CKIPing:  '+ row['內容']
		CkipDataContent = ''
		for sentence in ckip_json['result']:
			for term in sentence:
				if term['pos']=='N' or term['pos'] == 'Vi' or term['pos'] == 'Vt':
					CkipDataContent += '-'+term['term']
					term_frequency[term['term']]+=1
		
		data+=CkipDataContent+'\n'
	
	ckiped_data = open('CkipedData.csv','w')
	ckiped_data.write(data)
	ckiped_data.close()

	data_for_term = ''
	for word in term_frequency:
		data_for_term += word+':'+str(term_frequency[word])+'\n'

	term_freq = open('TermFerq.txt','w')
	term_freq.write(data_for_term)
	term_freq.close()


def FilterWord():
	term_freq_table = open('TermFerq.txt','r')
	term_frequency = defaultdict( int )
	for row in term_freq_table:
		row = row.split(':')
		term_frequency[row[0]]=row[1]

	trash_word = TrashWord()
	filtered_term_table = open('FilteredTermTable.txt','w')
	for key in term_frequency:
		if key not in trash_word:
			if term_frequency[key]>TERM_FREQ_THRESHOLE:
				filtered_term_table.write(str(key)+':'+str(term_frequency[key])+'\n')
			else:
				print 'filter out: '+key
		else:
			print 'filter out: '+key
	filtered_term_table.close()

def TrashWord():
	f_trash = open( TRASH_WORD_FILE ,'r')
	TrashWord = []
	for row in f_trash:
		TrashWord.append(re.sub(r"\n", "", row ))
	return TrashWord

def CkipReturn(in_text): #in_text is string
	segmenter = CKIPSegmenter('changcheng.tu', 'a10206606')
	try:
		segmented_in_text_result = segmenter.process(unicode(in_text))
	except:
		segmented_in_text_result = segmenter.process(unicode('got an error'))
	return segmented_in_text_result

def CreateBasket(term_table,data_table):
	feature_set = [] #for possible bursty feature which total frequency is more than 2
	syn_dict = Synonym()
	f = open(term_table,'r') #termset
	df = open(data_table,'r')
	term_post_table = open('TermPost.basket','w')
	for row in f:
		term = row.split(':')
		if term[0] in syn_dict:
			if syn_dict[term[0]] not in feature_set:
				feature_set.append(syn_dict[term[0]])
		else:
			feature_set.append(term[0])
	data=''
	for row in csv.DictReader(df):
		token = str(row['CkipDataContent']).split('-')
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


def Synonym():
	f = open( SYNONYM_FILE ,'r')
	syn_dict = defaultdict(str)
	for row in f:
		syn = row.split(':')
		syn_dict[syn[0]]=syn[1]

	return syn_dict

CkipCrawlerData('Opview.csv')
FilterWord()
#CreateTable('FilteredTermTable.txt','CkipCrawlerDataTable.csv')
CreateBasket('FilteredTermTable.txt','CkipedData.csv')
#Synonym('test')
