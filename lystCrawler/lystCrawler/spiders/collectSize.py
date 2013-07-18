from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http.request import Request
from lystCrawler.items import SizeItem
import urlparse, unicodedata
import unicodedata, math, urllib2

class LysSizeSpider(BaseSpider):
	name = "size"
	allowed_domains = ["oxygenboutique.com"]
	start_urls = [	"http://www.oxygenboutique.com/"
		     ]


	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		home_page = hxs.select("//body[@id='home_page']")
		product_page = hxs.select("//body[@id='product_page']")
		
		navLinks = hxs.select("//ul[@class='topnav']//a")
		productLinks = hxs.select("//div[@class='itm']//a")	
		
		#print "HomePage: ", len(home_page)
		#print "productPage: ", len(product_page)
		#print "Site Links: ", len(navLinks)
		#print "Product Links: ", len(productLinks) 

		if(home_page):
			for site in navLinks:
				print site
				print "Home Page yields ", site.select('@href').extract()
				url = site.select('@href').extract()[0]
				absolute_url = urlparse.urljoin(response.url, url.strip())
				yield Request(absolute_url, self.parse)
			
		if(product_page):
			item = SizeItem()
			#StockStatus
			request = urllib2.Request(response.url)
			urlOpen = urllib2.urlopen(request)
			headers = urlOpen.info()
			size = headers.getheader("last-modified")
			yield item

		else:
			for site in productLinks:
				print "ProductLinks extracts ", site.select('@href').extract()
				url = site.select('@href').extract()[0]
				absolute_url = urlparse.urljoin(response.url, url.strip())
				yield Request(absolute_url, self.parse)	


    	def replaceString(self, string):
		string = string.rstrip().lstrip()
		return string

