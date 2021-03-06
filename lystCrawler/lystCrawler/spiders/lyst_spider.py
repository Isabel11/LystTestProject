from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http.request import Request
from lystCrawler.items import OxyItem
import urlparse
import unicodedata 
import urllib2
import datetime


class LystSpider(BaseSpider):
	""" The spider that crawls the oxygenboutique site, extracts all products and submits it to the web service"""

	name = "lyst"
	allowed_domains = ["oxygenboutique.com"]
	start_urls = ["http://www.oxygenboutique.com/Dalila-Gold-Cap-Lace-Up-Flats.aspx"]


	def parse(self, response):
		"""	there are three different types of pages: the home page a product page and the product links (collection of all products)
		   	if the url is the home page the crawler goes through the top navigation bar and  opens all product link pages (recursively)
			on the product links pages the crawler finds the products for a specific type, e.g. dresses and calls on every single product (recursively)
		"""
		hxs = HtmlXPathSelector(response)
		home_page = hxs.select("//body[@id='home_page']")
		product_page = hxs.select("//body[@id='product_page']")
		
		navLinks = hxs.select("//ul[@class='topnav']//a")
		productLinks = hxs.select("//div[@class='itm']//a")	

		if(home_page):
			for site in navLinks:
				print site
				print "Home Page yields ", site.select('@href').extract()
				url = site.select('@href').extract()[0]
				absolute_url = urlparse.urljoin(response.url, url.strip())
				yield Request(absolute_url, self.parse)
			
		if(product_page):
			item = OxyItem()
			
			
			#Code
			item['code'] = hxs.select("//body/form/@action").extract()
			
			#Description
			item['description'] = hxs.select("//div[@id='accordion']/div[1]/span[1]/text()").extract()
			if(len(item['description']) == 0):
				item['description'] = hxs.select("//div[@id='accordion']/div[1]/text()").extract()

			#Price
			price = hxs.select("//span[@class='price geo_16_darkbrown']/text()").extract()
			price[0] = unicodedata.normalize('NFKD', price[0]).encode('ascii','ignore').rstrip().lstrip()
			if(price[0] == ''):
				item['gbp_price'] = hxs.select("//span[@class='offsetMark']/text()").extract()
			else:
			   item['gbp_price'] = price[0]

			#Designer
			item['designer'] = hxs.select("//a[@id='ctl00_ContentPlaceHolder1_AnchorDesigner']/text()").extract()

			#Gender			
			item['gender'] = 'F'
			
			#Images
			images = hxs.select("//div[@id='thumbnails-container']//td/a/@href").extract()
			item['image_urls'] = [urlparse.urljoin(response.url, image.strip()) for image in images]
			
			#Name
			item['name'] = hxs.select("//div[@id='breadcrumbs_2']/text()").extract()

			#Sale-discount
			item['sale_discount'] = hxs.select("//span[@class='price geo_16_darkbrown']/span[2]/text()").extract()
			
			#sourceURL
			item['source_url'] = response.url

			#StockStatus
			sizes = hxs.select("//select[@id='ctl00_ContentPlaceHolder1_ddlSize']/option")
			size_dict = {}
			for size in sizes:
				option = size.select('@value').extract()[0]
				value = size.select('text()').extract()[0]
				if(option == "-1"):
					pass
				elif(option == "0"):
					size_dict[value] = 1
				else:
					size_dict[value] = 3
			item['stock_status']  = size_dict

			#Last Updated
			dateFromHeader = response.headers['date']
			formatted = datetime.datetime.strptime(dateFromHeader, "%a, %d %b %Y %H:%M:%S GMT")			
			item['last_updated'] = formatted.strftime("%Y-%m-%d %H:%M:%S")

			yield item
		else:
			for site in productLinks:
				print "ProductLinks extracts ", site.select('@href').extract()
				url = site.select('@href').extract()[0]
				absolute_url = urlparse.urljoin(response.url, url.strip())
				yield Request(absolute_url, self.parse)	



