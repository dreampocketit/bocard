#-*- coding: utf-8 -*-
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from fjsen.items import FjsenItem
from scrapy.selector import Selector
from scrapy.http import Request

class FjsenSpider(BaseSpider):
	name="fjsen1"
	allowed_domains=["fjsen.com"]
	start_urls=['http://www.sogi.com.tw/mobile/forums/3463?hall_type=phone&page='+str(x) for x in range(1,138)]+['http://www.sogi.com.tw/mobile/forums/3463?hall_type=phone&page=']

	def parse(self,response):
		sel = Selector(response)
		sites = sel.xpath('//td[@class="col3"]')
		items=[]
		for site in sites:
			item=FjsenItem()
			item['title']= site.xpath('a/text()').extract()
			title = site.xpath('a/text()').extract()
			print 'hahaha'
			link = site.xpath('a/@href').extract()
			link_complete = "http://www.sogi.com.tw" + link[0]
			#print link
			return Request(link_complete, callback = self.visit_b_page)
			#print link
		#return items

	def visit_b_page(self,response):
		item = response.meta['item']
		item['other_url'] = response.url
		return item
		#print 'hahaha'
		#return 'hahaha'
		#self.log("Visited %s" % response.url)
