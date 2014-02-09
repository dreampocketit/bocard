# Scrapy settings for crawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'crawler'

SPIDER_MODULES = ['crawler.spiders']
NEWSPIDER_MODULE = 'crawler.spiders'

DATABASE = {'drivername': '111',
            'username': 'yyy',
            'password': 'zzz',
			'database': 'vvv'}

ITEM_PIPELINES = {
    'crawler.pipelines.CrawlerPipeline':300
}
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'crawler (+http://www.yourdomain.com)'
