# -*- coding: utf-8 -*-
import scrapy
import urllib
from keywordsearch.items import KeywordsearchItem

class NytimesSpider(scrapy.Spider):
    name = "nytimes"
    allowed_domains = ["nytimes.com"]
    basic_url = "http://query.nytimes.com/search/sitesearch/?#/"
    query = 'microsoft'
    dateRange = '7days'

    def start_requests(self):
        url = self.basic_url + self.query + '/' + self.dateRange + '/allresults/'
        for n in ['1/', '2/']:
            yield scrapy.Request(url + n, self.parse, dont_filter=True, meta={'phantomjs': True, 'target': 'nytimes'})
    
    def parse(self, response):
        for url in response.xpath('//div[@id="searchResults"]//h3/a/@href').extract():
            yield scrapy.Request(response.urljoin(url), self.parse_article, meta={'phantomjs': True, 'target': 'nytimes'}, headers={'Referer': 'https://www.google.com'})
    
    def parse_article(self, response):
        item = KeywordsearchItem()
        item['title'] = response.xpath('//h1[@id="headline"]/text()').extract()
        header = response.xpath('//div[@id="story-meta-footer"]')
        item['author'] = header.xpath('//span[@itemprop="name"]/text()').extract()
        item['time'] = header.xpath('p/time/text()')[0].extract()
        item['content'] = response.xpath('//div[@class="story-body"]/p/text()').extract()
        item['url'] = response.url
        item['publisher'] = 'NYTimes'
        item['query'] = self.query
        yield item