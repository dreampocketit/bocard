#-*- coding: utf-8 -*-

from fjsen.items import FjsenItem
from scrapy.selector import Selector

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.http import FormRequest
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy import log
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class FjsenSpider(CrawlSpider):
	name = "fjsen"
	allowed_domains = ["sogi.com.tw"]
	#start_urls=['http://www.sogi.com.tw/mobile/forums/3463?hall_type=phone&page='+str(x) for x in range(1,138)]+['http://www.sogi.com.tw/mobile/forums/3463?hall_type=phone&page=']
	start_urls = [
		#"http://www.statesassembly.gov.je/Pages/Hansard.aspx?page=1"
		#"http://acg.gamer.com.tw/index.php?page=3&p=OLG&t=1&tnum=1933"
		#"http://www.babyhome.com.tw/mboard/list.php?bid=15&style=education&page=1"
		"http://www.sogi.com.tw/mobile/forums/3463?hall_type=phone&page=1"
	]
	rules = (
		#Rule(SgmlLinkExtractor(allow=('/forums/3463?hall_type=phone&page=*',),unique=True)),
		Rule(SgmlLinkExtractor(allow=('page=*',),deny=('fontSize=*', ),unique=True)),
 
        #When we get to specific doc do this
        Rule(SgmlLinkExtractor(allow=('/mobile/articles/*', )), callback='parse_hansard_item'),

	)

	#def parse(self, response):
	#	self.log('parse_hansard_item called for: %s' % response.url, level=log.INFO)
	#	sel = Selector(response)
	#	item=FjsenItem()
	#	content = sel.xpath('//*[@class="txt-bold"]/text()').extract()
	#	print content

	def parse_hansard_item(self, response):
		self.log('parse_hansard_item called for: %s' % response.url, level=log.INFO)
		sel = Selector(response)
		items = []
		item=FjsenItem()
		#item['title']= site.xpath('a/text()').extract()
		item['title']= sel.xpath('//*[@class="clearfix"]/h2/text()').extract()
		title = sel.xpath('//*[@class="clearfix"]/h2/text()').extract()
		#print title
		content = ""
		for ele in sel.xpath('//*[@class="content"]/text()').extract():
			content = content + ele
		item['context']= content
		context = sel.xpath('//*[@id="main"]/div/article/section/div[1]/article/div[2]/div/text()').extract()
		#print item['context']
		item['source']= "Apple iphone"
		item['sourcetype']= "Forum-手機王"
		item['mainbody']= "True"
		#print context
		item['date']= sel.xpath('//*[@id="main"]/div/article/section/div[1]/article/div[1]/p[3]/span/text()').extract()[0].replace('發表時間:','').replace(' +0800','+0800')
		date = sel.xpath('//*[@id="main"]/div/article/section/div[1]/article/div[1]/p[3]/span/text()').extract()
		#print item['date'][0].replace('發表時間:','')
		item['author']= sel.xpath('//*[@id="main"]/div/article/section/div[1]/article/div[1]/p[1]/a/text()').extract()
		author = sel.xpath('//*[@id="main"]/div/article/section/div[1]/article/div[1]/p[1]/a/text()').extract()

		item['link']= "www.google.com.tw"

		items.append(item)
		
		return item
		
