# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field



class OxyItem(Item):
	code = Field()
	description = Field()
	designer = Field()	
	gbp_price = Field()
	gender = Field()
	image_urls = Field()
	name = Field()
	raw_color = Field()
	sale_discount= Field()
	source_url = Field()
	stock_status = Field()
	last_updated = Field()
	type = Field()


class SizeItem(Item):
	size = Field()
