# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3
from os import path
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

class FjsenPipeline(object):

	filename = '/root/dreampocket/dp.db'
	#filename = 'dp.db'

	def __init__(self):
		self.conn=None
		dispatcher.connect(self.initialize,signals.engine_started)
		dispatcher.connect(self.finalize,signals.engine_stopped)
		

	def process_item(self, item, spider):
		self.conn.execute('insert into warehouse_rawdata values(?,?,?,?,?,?,?,?,?)',(None,item['title'][0],item['context'],item['source'][0],item['sourcetype'][0],item['mainbody'][0],item['date'],item['author'][0],item['link'][0]))
		self.conn.commit()
		return item

	def initialize(self):
		if path.exists(self.filename):
			self.conn=sqlite3.connect(self.filename)
		else:
			self.conn=self.create_table(self.filename)

	def finalize(self):
		if self.conn is not None:
			self.conn.commit()
			self.conn.close()
			self.conn=None

	def create_table(self,filename):
		print 'db is not existed'
#		conn=sqlite3.connect(filename)
#		conn.execute("""create table fjsen(id integer primary key autoincrement,title text,link text,addtime text)""")
#		conn.commit()
#		return conn
