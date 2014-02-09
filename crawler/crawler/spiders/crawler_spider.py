from soup import BeautifulSoup as bs
from scrapy.http import Request
from scrapy.spider import BaseSpider
from crawler.items import CrawlerItem
 
class CrawlerSpider(BaseSpider):
    name = 'crawler'
    allowed_domains = []
    start_urls = ['http://news.ycombinator.com']
 
    def parse(self, response):
        if 'news.ycombinator.com' in response.url:
            soup = bs(response.body)
            items = [(x[0].text, x[0].get('href')) for x in
                     filter(None, [
                         x.findChildren() for x in
                         soup.findAll('td', {'class': 'title'})
                     ])]
 
            for item in items:
                print item
                crawler_item = CrawlerItem()
                crawler_item['title'] = item[0]
                crawler_item['link'] = item[1]
                try:
                    yield Request(item[1], callback=self.parse)
                except ValueError:
                    yield Request('http://news.ycombinator.com/' + item[1], callback=self.parse)
 
                yield crawler_item

