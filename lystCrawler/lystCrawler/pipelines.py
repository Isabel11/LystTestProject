# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
import unicodedata, math, re, json, httplib
from lystCrawler.items import OxyItem
from scrapy.contrib.exporter import JsonItemExporter
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals



class CleanUpHTMLPipeline(object):
    def process_item(self, item, spider):
	for key, value in item.iteritems():
		if(key == 'stock_status'):
			for dict_key in value:
				if isinstance(dict_key, unicode):
					new_key = self.replaceString(unicodedata.normalize('NFKD', dict_key).encode('ascii','ignore')).replace(' - Sold Out','')
				else:
					new_key = self.replaceString(dict_key).replace(' - Sold Out','')
				value[new_key] = value.pop(dict_key)

		elif(isinstance(value, str)):
			item[key] = self.replaceString(value)
		else:	
			item[key] = [self.replaceString(unicodedata.normalize('NFKD', v).encode('ascii','ignore')) for v in value]
			item[key] = filter(lambda empty: empty.strip(), item[key])
			if(len(item[key]) == 1): item[key] = item[key][0]
			if(len(item[key]) == 0): item[key] = '' 
	return item

    def replaceString(self, string):
	string = string.rstrip().lstrip()
	return string

class DeterminePriceAndDiscountPipeline(object):
	def process_item(self, item, spider):
		if(len(item['sale_discount'])==0): item['sale_discount'] = '0.0'
		else:		
			discount = (float(item['gbp_price']) - float(item['sale_discount']))
			item['sale_discount'] = str(round((discount/float(item['gbp_price']))*100))
		return item

class FormatCodePipeline(object):
	def process_item(self, item, spider):
		item['code'] = item['code'].replace('/','').replace('.aspx','')
		return item



class PUTPipeline(object):
	def process_item(self, item, spider):
		print "PUT products"
		data_json = json.dumps(dict(item))
		connection =  httplib.HTTPConnection('localhost:5000')
		connection.request('PUT', '/rest/products/', data_json)
		postResult = connection.getresponse()
		connection.close()
		return item

class JsonExportPipeline(object):

    def __init__(self):
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        self.files = {}

    def spider_opened(self, spider):
        file = open('%s_items.json' % spider.name, 'w+b')
        self.files[spider] = file
        self.exporter = JsonItemExporter(file)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

SHOES =re.compile (r'\b[s|S]{1}hoe[s]*\b|\b[w|W]{1}edge[s]*\b|\b[b|B]{1}oot[s]*\b|\b[b|B]{1}ootie[s]*\b|\b[p|P]{1}ump[s]*\b|\b[h|H]{1}eel[s]*\b|\b[s|S]{1}neaker[s]*\b')
JEWELRY = re.compile(r'\b[b|B]{1}racelet[s]*\b|\b[n|N]{1}ecklace[s]*\b|\b[r|R]{1}ing[s]*\b|\b[e|E]{1}arring[s]*\b')
BAGS = re.compile(r'\b[b|B]{1}ag[s]*\b')
ACCESSORIES = re.compile(r'\b[s|S]{1}unglasses{1}|[h|H]{1}at[s]*\b')	

class DetermineType(object):
	def process_item(self, item, spider):
		s = re.findall(SHOES, item['description'])
		b = re.findall(BAGS, item['description'])
		j = re.findall(BAGS, item['description'])
		r = re.findall(BAGS, item['description'])
		if (len(s) > 0):
			item['type']='S'
		elif (len(b) > 0):
			item['type']='B'
		elif (len(j) > 0):
			item['type']='J'
		elif (len(r) > 0):
			item['type']='R'
		else:
			item['type'] = 'A'
		return item


class FindColor(object):
	def process_item(self, item, spider):
		
		color = ''
		if(len(re.findall(re.compile(r'\bblack\b'),item['description']))):
			color+= 'black '
		if(len(re.findall(re.compile(r'\white\b'),item['description']))):
			color+= 'white '
		if(len(re.findall(re.compile(r'\bbeige\b'),item['description']))):
			color+= 'beige '
		if(len(re.findall(re.compile(r'\bsilver\b'),item['description']))):
			color+= 'silver '
		if(len(re.findall(re.compile(r'\bgray\b'),item['description']))):
			color+= 'gray '
		if(len(re.findall(re.compile(r'\bnavy\b'),item['description']))):
			color+= 'navy '
		if(len(re.findall(re.compile(r'\bblue\b'),item['description']))):
			color+= 'blue '
		if(len(re.findall(re.compile(r'\bgreen\b'),item['description']))):
			color+= 'green '
		if(len(re.findall(re.compile(r'\bolive\b'),item['description']))):
			color+= 'olive '
		if(len(re.findall(re.compile(r'\bgolden\b'),item['description']))):
			color+= 'golden '
		if(len(re.findall(re.compile(r'\bcoral\b'),item['description']))):
			color+= 'coral '
		if(len(re.findall(re.compile(r'\bpink\b'),item['description']))):
			color+= 'pink '
		if(len(re.findall(re.compile(r'\bred\b'),item['description']))):
			color+= 'red '
		if(len(re.findall(re.compile(r'\byellow\b'),item['description']))):
			color+= 'yellow '
		if(len(re.findall(re.compile(r'\bviolet\b'),item['description']))):
			color+= 'violet '
		if(len(re.findall(re.compile(r'\bbrown\b'),item['description']))):
			color+= 'brown '
		if(len(re.findall(re.compile(r'\bmaroon\b'),item['description']))):
			color+= 'maroon '
		if(len(re.findall(re.compile(r'\bcreme\b'),item['description']))):
			color+= 'creme '
		if(color == ""):
			color+= 'def_color'

		item['raw_color'] = color
		return item

