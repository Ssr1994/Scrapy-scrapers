# -*- coding: utf-8 -*-
import scrapy
import urllib
import re
from keywordsearch.items import KeywordsearchItem
from keywordsearch.settings import QUERY, FILE_PATH

class CnnSpider(scrapy.Spider):
    name = "cnn"
    allowed_domains = ["cnn.com"]
    basic_url = "http://www.cnn.com/search/?text="

    def start_requests(self):
        # CNN's date range is handled in middlewares.py
        for n in [1, 2]:
            yield scrapy.Request(self.basic_url + urllib.quote_plus(QUERY), self.parse, dont_filter=True,
                                 meta={"phantomjs": True, 'target': 'cnn', 'pageNum': n})
    
    def parse(self, response):
        for url in response.xpath('//h3[@class="cd__headline"]/a/@href').extract():
            yield scrapy.Request(response.urljoin(url), self.parse_article)
    
    def parse_article(self, response):
        urlSplit = response.url.split('/')
        if urlSplit[3] == 'videos':
            return
        
        item = KeywordsearchItem()
        if urlSplit[6] == 'opinions':
            item['title'] = response.xpath('//h1[@class="pg-headline"]/text()').extract()
            item['author'] = response.xpath('//span[@class="metadata__byline__author"]/a/text()').extract()
            item['time'] = response.xpath('//p[@class="update-time"]/text()').extract()
            item['keyLine'] = ''
            item['content'] = ' '.join(response.xpath('//p[@class="zn-body__paragraph"]//text()').extract())
        else:
            item['title'] = response.xpath('//h1[@class="article-title"]/text()').extract()
            item['author'] = response.xpath('//span[@class="cnnbyline "]/span[@class="byline"]/a/text()').extract()
            body = response.css('#storytext')
            item['keyLine'] = body.xpath('h2/text()').extract()
            item['content'] = ' '.join(body.xpath('p//text()').extract())
            item['time'] = response.xpath('//div[@class="storytimestamp"]/span[@class="cnnDateStamp"]/text()').extract()
        item['url'] = response.url
        item['publisher'] = 'CNN'
        item['query'] = QUERY
        item['title'] = ''.join(item['title'])
        with open(FILE_PATH + re.sub('[:/]', '', item['title']) + '.html', 'w') as f:
            f.write(response.body)
        yield item