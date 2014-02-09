# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy.orm import sessionmaker
from models import Crawler, db_connect, create_crawler_table

class CrawlerPipeline(object):
	def __init__(self):
		engine = db_connect()
		create_crawler_table(engine)
		self.Session = sessionmaker(bind=engine)

	def process_item(self, item, spider):
		session = self.Session()
		crawler = Crawler(**item)
		session.add(crawler)
		session.commit()
		return item
