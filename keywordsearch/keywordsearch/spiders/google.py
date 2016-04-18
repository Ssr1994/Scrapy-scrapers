# -*- coding: utf-8 -*-
import scrapy


class GoogleSpider(scrapy.Spider):
    name = "google"
    allowed_domains = ["google.com"]

    def parse(self, response):
        pass
