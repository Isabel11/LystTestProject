# Scrapy settings for lystCrawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'lystCrawler'

SPIDER_MODULES = ['lystCrawler.spiders']
NEWSPIDER_MODULE = 'lystCrawler.spiders'


ITEM_PIPELINES = ['lystCrawler.pipelines.CleanUpHTMLPipeline', 
		  'lystCrawler.pipelines.DeterminePriceAndDiscountPipeline',
		  'lystCrawler.pipelines.FormatCodePipeline',
		  'lystCrawler.pipelines.DetermineTypePipeline',
		  'lystCrawler.pipelines.DetermineColorPipeline',
		  'lystCrawler.pipelines.PUTPipeline']

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'lystCrawler (+http://www.yourdomain.com)'
