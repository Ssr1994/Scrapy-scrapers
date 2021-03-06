# -*- coding: utf-8 -*-
import scrapy
import urllib
import re
from keywordsearch.items import KeywordsearchItem
from keywordsearch.settings import QUERY, FILE_PATH

class NytimesSpider(scrapy.Spider):
    name = "nytimes"
    allowed_domains = ["nytimes.com"]
    basic_url = "http://query.nytimes.com/search/sitesearch/?#/"
    dateRange = '7days'

    def start_requests(self):
        url = self.basic_url + QUERY + '/' + self.dateRange + '/allresults/'
        for n in ['1/', '2/']:
            yield scrapy.Request(url + n, self.parse, dont_filter=True, meta={'phantomjs': True})
    
    def parse(self, response):
        for url in response.xpath('//div[@id="searchResults"]//h3/a/@href').extract():
            yield scrapy.Request(response.urljoin(url), self.parse_article, meta={'target': 'nytimes'})
    
    def parse_article(self, response):
        item = KeywordsearchItem()
        item['title'] = ''.join(response.xpath('//h1[@id="headline"]/text()').extract()).lstrip()
        header = response.xpath('//div[@id="story-meta-footer"]')
        item['author'] = header.xpath('//span[@itemprop="name"]/text()').extract()
        item['time'] = header.xpath('p/time/text()').extract()
        item['content'] = response.xpath('//div[@class="story-body"]/p//text()').extract()
        item['url'] = response.url
        item['publisher'] = 'NYTimes'
        item['query'] = QUERY
        item['keyLine'] = ''
        with open(FILE_PATH + re.sub('[:/]', '', item['title']) + '.html', 'w') as f:
            f.write(response.body)
        yield item