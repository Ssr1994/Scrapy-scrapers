# -*- coding: utf-8 -*-
import scrapy
import urllib
import re
from datetime import date, timedelta
from keywordsearch.items import KeywordsearchItem
from keywordsearch.settings import QUERY, FILE_PATH

class FoxnewsSpider(scrapy.Spider):
    name = "foxnews"
    orgname = "Fox News"
    allowed_domains = ["foxnews.com"]
    query_url = "http://www.foxnews.com/search-results/search?q="
    days = 14

    def start_requests(self):
        end_date = date.today()
        start_date = end_date - timedelta(self.days)
        options = "&ss=fn&min_date=" + start_date.isoformat() + "&max_date=" + end_date.isoformat() + "&start="
        for n in ['0', '10']:
            yield scrapy.Request(self.query_url + urllib.quote(QUERY) + options + n, 
                                 callback=self.parse, meta={"phantomjs": True})

    def parse(self, response):
        for sel in response.xpath('//div[@class="search-info responsive-image"]'):
            url = ''.join(sel.xpath('./h3/a/@href').extract()).encode('ascii')
            keyline = ''.join(sel.xpath('./p/text()').extract())
            yield scrapy.Request(url.encode('ascii'), self.parse_article, meta={"keyline": keyline})
        for sel in response.xpath('//div[@class="search-info"]'):
            url = ''.join(sel.xpath('./h3/a/@href').extract()).encode('ascii')
            keyline = ''.join(sel.xpath('./p/text()').extract())
            yield scrapy.Request(url, self.parse_article, meta={"keyline": keyline})

    def parse_article(self, response):
        # jQuery on fox's page returns duplicate pages
        item = KeywordsearchItem()
        item['title'] = ''.join(response.xpath('//div[@class="main"]//h1/text()').extract()).lstrip()
        item['author'] = response.xpath('//div[@class="article-info"]//a/text()').extract()
        if not item['author']:
            item['author'] = response.xpath('//div[@class="article-info"]/div/div/text()').extract()
        if not item['author']:
            item['author'] = response.xpath('//div[@class="article-info"]/div/p/span/text()').extract()
        item['time'] = response.xpath('//div[@class="article-info"]//time/@datetime').extract()
        item['publisher'] = self.orgname
        item['url'] = response.url
        item['content'] = ' '.join(response.xpath('//div[@itemprop="articleBody"]/p//text()').extract())
        if not item['content']:
            item['content'] = ' '.join(response.xpath('//div[@class="article-text"]/p//text()').extract())
        item['query'] = QUERY
        item['keyLine'] = response.meta['keyline']
        with open(FILE_PATH + re.sub('[:/]', '', item['title']) + '.html', 'w') as f:
            f.write(response.body)
        yield item