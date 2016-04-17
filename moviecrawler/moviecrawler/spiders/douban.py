# -*- coding: utf-8 -*-
import scrapy
from moviecrawler.items import DoubanItem

class DoubanSpider(scrapy.Spider):
    name = "douban"
    allowed_domains = ["douban.com"]
    start_urls = (
        'https://movie.douban.com/top250/',
    )

    def parse(self, response):
        for sel in response.xpath('//ol[@class="grid_view"]/li'):
            info = sel.xpath('div/div[@class="info"]')
            href = info.xpath('div[@class="hd"]/a/@href')[0].extract()
            item = DoubanItem()
            item['rating'] = info.xpath('div[@class="bd"]/div/span[@class="rating_num"]/text()').extract()
            item['quote'] = info.xpath('div[@class="bd"]/p[@class="quote"]/span/text()').extract()
            yield scrapy.Request(response.urljoin(href), callback=self.parse_contents, meta={'item': item})

        nextPage = response.xpath('//div[@class="paginator"]/span[@class="next"]/a/@href')
        if nextPage:
            yield scrapy.Request(response.urljoin(nextPage[0].extract()), callback=self.parse)
    
    def parse_contents(self, response):
        item = response.meta['item']
        item['title'] = response.xpath('//h1/span[@property="v:itemreviewed"]/text()').extract()
        item['year'] = response.xpath('//h1/span[@class="year"]/text()').re('\d+')
        info = response.css('#info')
        item['director'] = info.xpath('span[1]/span[2]/a/text()').extract()
        item['writer'] = info.xpath('span[2]/span[2]/a/text()').extract()
        item['star'] = info.xpath('span[3]/span[2]/a[position()<4]/text()').extract()
        item['genre'] = info.xpath('span[@property="v:genre"]/text()').extract()
        item['link'] = info.xpath('a/@href').extract()
        yield item
