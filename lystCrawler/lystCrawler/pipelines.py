# Pipelines for items
import unicodedata
import math
import re
import json
import httplib
from lystCrawler.items import OxyItem
from scrapy.contrib.exporter import JsonItemExporter
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from regex import itemAttributes



class CleanUpHTMLPipeline(object):
   """removes empty space, newlines etc and converts unicode into string for later processing"""

	def process_item(self, item, spider):
		for key, value in item.iteritems():
			if(key == 'stock_status'):		
				for dict_key in value:
					if isinstance(dict_key, unicode):
						new_key = self.__stripString(unicodedata.normalize('NFKD', dict_key).encode('ascii','ignore')).replace(' - Sold Out','')
					else:
						new_key = self.__stripString(dict_key).replace(' - Sold Out','')
					value[new_key] = value.pop(dict_key)
	
			elif(isinstance(value, str)):
				item[key] = self.__stripString(value)
			else:	
				item[key] = [self.__stripString(unicodedata.normalize('NFKD', v).encode('ascii','ignore')) for v in value]
				item[key] = filter(lambda empty: empty.strip(), item[key])
				if(len(item[key]) == 1): item[key] = item[key][0]
				if(len(item[key]) == 0): item[key] = '' 
		return item

 	   def __stripString(self, string):
		string = string.rstrip().lstrip()
		return string

class DeterminePriceAndDiscountPipeline(object):
	"""" recalculates price if there is a discount"""

	def process_item(self, item, spider):
		if(len(item['sale_discount'])==0): item['sale_discount'] = '0.0'
		else:		
			discount = (float(item['gbp_price']) - float(item['sale_discount']))
			item['sale_discount'] = str(round((discount / float(item['gbp_price'])) * 100))
		return item

class FormatCodePipeline(object):
	""" formats the type code (just removing the .aspx and a slash)"""

	def process_item(self, item, spider):
		item['code'] = item['code'].replace('/','').replace('.aspx','')
		return item

class DetermineTypePipeline(object):
	""" determines the type of an object (using class regex)"""

	def process_item(self, item, spider):
		iType = itemAttributes()
		item['type'] = iType.findType(item['description'])
		return item

class DetermineColorPipeline(object):
	""" determines the color of an object (using class regex)"""

	def process_item(self, item, spider):
		cType = itemAttributes()
		item['raw_color'] = cType.findColor(item['description'])
		return item

class PUTPipeline(object):
	""" connects to the web service and submits the item using PUT """

	def process_item(self, item, spider):
		data_json = json.dumps(dict(item))
		connection =  httplib.HTTPConnection('localhost:5000')
		connection.request('PUT', '/rest/products/', data_json)
		postResult = connection.getresponse()
		connection.close()
		return item



