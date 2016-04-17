# -*- coding: utf-8 -*-
import scrapy
from moviecrawler.items import ImdbItem

class ImdbSpider(scrapy.Spider):
    name = "imdb"
    allowed_domains = ["imdb.com"]
    start_urls = (
        'http://www.imdb.com/chart/top/',
    )

    def parse(self, response):
        for sel in response.xpath('//tbody[@class="lister-list"]/tr'):
            item = ImdbItem()
            titleColumn = sel.xpath('td[@class="titleColumn"]')
            item['title'] = titleColumn.xpath('a/text()').extract()
            item['year'] = titleColumn.xpath('span/text()').re('\d+')
            item['cast'] = titleColumn.xpath('a/@title').extract()
            item['rating'] = sel.xpath('td[@class="ratingColumn imdbRating"]/strong/text()').extract()
            yield item
