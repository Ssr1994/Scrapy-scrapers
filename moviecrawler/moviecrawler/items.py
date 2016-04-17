# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ImdbItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    year = scrapy.Field()
    cast = scrapy.Field()
    rating = scrapy.Field()

class DoubanItem(scrapy.Item):
    title = scrapy.Field()
    year = scrapy.Field()
    rating = scrapy.Field()
    director = scrapy.Field()
    writer = scrapy.Field()
    star = scrapy.Field()
    genre = scrapy.Field()
    quote = scrapy.Field()
    link = scrapy.Field()