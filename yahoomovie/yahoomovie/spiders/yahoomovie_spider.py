#-*- coding: utf-8 -*-

from yahoomovie.items import YahoomovieItem
from scrapy.selector import Selector
import re
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.http import FormRequest
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy import log
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class YahoomovieSpider(CrawlSpider):
	global data	
	data = "datacontent,sentiment\n"
	name = "yahoomovie"
	data = "datacontent,sentiment\n"
	allowed_domains = ["yahoo.com"]

	start_urls = [
        #"http://www.statesassembly.gov.je/Pages/Hansard.aspx?page=1"
        #"http://www.sogi.com.tw/mobile/forums/3463?hall_type=phone&page=1"
		#"http://tw.movie.yahoo.com/chart.html?cate=taipei",
		"http://tw.movie.yahoo.com/movieinfo_review.html/id=4920&s=0&o=0&p=1"
	]
	rules = (
		#Rule(SgmlLinkExtractor(allow=('movieinfo_main.html/id=4920',))),
		#Rule(SgmlLinkExtractor(allow=('movieinfo_review.html/id=4920', ))),
		Rule(SgmlLinkExtractor(allow=('id=4920&s=0*', )), callback='parse_review_item'),
	)


	def parse_review_item(self, response):
		global data
		#data = "datacontent,sentiment\n"
		self.log('parse_review_item called for: %s' % response.url, level=log.INFO)
		sel = Selector(response)
		items = []
		score= []
		item = YahoomovieItem()
		print '*****************************************'	
		content = ""
		#for ele in sel.xpath('//*[@class="text"]/h4/text()').extract():
		#	content = content + ele
		#item['context']= content
	
		item['title'] = sel.xpath('//*[@class="text"]/h4/text()').extract()
		#item['title'] = sel.xpath('//*[@id="ymvurl"]/div[2]/div/div/div/div/div[2]/h4/text()').extract()
		item['context'] = sel.xpath('//*[@class="text"]/p[1]/text()').extract()
		score_revise = ""
		for sco in sel.xpath('//*[@id="ymvurl"]/div[2]/div/div/div/div/div[1]/div[1]/img/@src').extract():
			score_revise = sco.replace('http://l.yimg.com/f/i/tw/movie/i6/rating_star_','').replace('.gif','')
			score.append(score_revise)
				
		#item['score'] = sel.xpath('//*[@id="ymvurl"]/div[2]/div/div/div/div/div[1]/div[1]/img/@src').extract()[1]
		item['score'] = score

		itemtitle = ""
		for count in range(len(item['score'])):
			#print item['title'][count]
			#print item['context'][count]
			tmp = item['context'][count].replace('\n','').replace('^M',',')
			data += tmp + ',' + item['score'][count] + '\n'
		
		for count in range(len(item['score'])):
			#print item['title'][count]
			#print item['context'][count]
			tmp = item['title'][count].replace('標題：','')
			data += tmp + ',' + item['score'][count] + '\n'
		
		yahoo_movie = open("Yahoo_Movie.csv",'w')
		yahoo_movie.write(data)
		yahoo_movie.close()		
		#print 'hahahahhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh'
		#items.append(item)
		#return item

