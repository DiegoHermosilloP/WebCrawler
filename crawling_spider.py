from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import scrapy

# Run in terminal the following command to receive the results: scrapy crawl wikipedia -o output.json 

class CrawlingSpider(CrawlSpider): #Inherits from the CrawlSpider class
    #Here is where the crawling is done
    name='wikipedia'
    custom_settings={'DEPTH_LIMIT':1,} #'AUTOTHROTTLE_TARGET_CONCURRENCY':2
    #The default of DEPTH_LIMIT is 0, so there is no limit. Avoid this for a big web page such as wikipedia
    allowed_domains=['es.wikipedia.org'] #Only allow Wikipedia domains in spanish
    start_urls=['https://es.wikipedia.org/wiki/Wikipedia:Portada']
    rules=(
        Rule(LinkExtractor(allow='/wiki/',deny='/wiki/File:'),callback="parse",follow=True),#all parameters are crucial, but 'follow' is what makes this a true crawler and not just a scraper
    )  

    def parse(self, response):
        #Here we do the scraping
        yield{
            "links":response.url,
            "titles":response.css('.mw-headline::text').getall(),
            'main_title':response.css('.mw-page-title-main::text').getall(),
            'text':''.join(response.css('p *::text').getall())
        }
#From terminal, the following commands can be done to explore on a specific url
# scrapy shell '__link__'
#response.css('x') 