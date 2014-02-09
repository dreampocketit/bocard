# Scrapy settings for fjsen project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'fjsen'

SPIDER_MODULES = ['fjsen.spiders']
NEWSPIDER_MODULE = 'fjsen.spiders'

ITEM_PIPELINES=['fjsen.pipelines.FjsenPipeline']
DOWNLOAD_DELAY = 0.75    # 250 ms of delay
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'fjsen (+http://www.yourdomain.com)'
