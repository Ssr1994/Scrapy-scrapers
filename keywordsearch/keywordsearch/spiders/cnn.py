# -*- coding: utf-8 -*-
import scrapy
import urllib
from keywordsearch.items import KeywordsearchItem

class CnnSpider(scrapy.Spider):
    name = "cnn"
    allowed_domains = ["cnn.com"]
    basic_url = "http://www.cnn.com/search/?text="
    query = 'microsoft'

    def start_requests(self):
        yield scrapy.Request(self.basic_url + urllib.quote_plus(self.query), self.parse)
    
    def parse(self, response):
        for url in response.xpath('//h3[@class="headline"]/a/@href').extract():
            yield scrapy.Request(response.urljoin(url), self.parse_article)
    
    def parse_article(self, response):
        item = KeywordsearchItem()
        
        item['url'] = response.url
        item['publisher'] = 'Wall Street Journal'
        item['query'] = self.query
        yield item
