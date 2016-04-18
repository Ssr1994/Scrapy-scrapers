# -*- coding: utf-8 -*-
import scrapy
from keywordsearch.items import KeywordsearchItem

class WapostSpider(scrapy.Spider):
    name = "wapost"
    allowed_domains = ["washingtonpost.com"]
    basic_url = 'http://www.washingtonpost.com/newssearch/?query=';
    keyword = 'google'

    def start_requests(self):
        yield scrapy.Request(self.basic_url + self.keyword, self.parse, meta={"phantomjs": True, "target": 'wapost'})
    
    def parse(self, response):
        for url in response.xpath('//div[@class="pb-results-container"]//a/@href').extract():
            yield scrapy.Request(response.urljoin(url), self.parse_article)
    
    def parse_article(self, response):
        item = KeywordsearchItem()
        item['title'] = response.xpath('//div[@id="article-topper"]/h1/text()').extract() #may be the same
        body = response.xpath('//div[@id="article-body"]')
        item['author'] = body.xpath('//span[@itemprop="name"]/text()').extract() #may need to take care of &thinsp;
        item['time'] = body.xpath('//span[@itemprop="datePublished"]/text()').extract()
        item['publisher'] = 'Washington Post'
        item['url'] = response.url
        item['content'] = ' '.join(body.xpath('article[@itemprop="articleBody"]/p/text()').extract())
        item['query'] = self.keyword
        yield item