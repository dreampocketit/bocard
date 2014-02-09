# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class FjsenItem(Item):
    # define the fields for your item here like:
    # name = Field()
	title = Field()
	context = Field(serializer=str)
	source = Field()
	sourcetype = Field()
	mainbody = Field()
	date = Field(serializer=str)
	author = Field()
	link=Field()
