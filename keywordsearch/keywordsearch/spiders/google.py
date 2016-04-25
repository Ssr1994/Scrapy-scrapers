# -*- coding: utf-8 -*-
import scrapy


class GoogleSpider(scrapy.Spider):
    name = "google"
    allowed_domains = ["google.com"]

    def start_requests(self):
        yield scrapy.Request("http://www.nytimes.com/2016/04/12/technology/personaltech/marking-up-web-pages-in-windows-10.html", self.parse)
    
    def parse(self, response):
        with open('./webpages/test.html', 'a') as f:
            f.write(response.body)
