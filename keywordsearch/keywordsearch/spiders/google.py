# -*- coding: utf-8 -*-
import scrapy


class GoogleSpider(scrapy.Spider):
    name = "google"
    allowed_domains = ["google.com"]

    def start_requests(self):
        yield scrapy.Request("https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&ved=0ahUKEwjQkZPnypnMAhVS3WMKHeKhCHAQFggdMAA&url=http%3A%2F%2Fwww.wsj.com%2Farticles%2Fmicrosoft-sues-justice-department-over-secret-customer-data-searches-1460649720&usg=AFQjCNGWoEwA13_NQ1My3yusraiu1jM-mw&sig2=8GHIoJ_P-iju7hfvl2b2Cw&cad=rjt", self.parse, meta={"phantomjs": True, "target": 'g'})
    
    def parse(self, response):
        print response.xpath('//div[@id="wsj-article-wrap"]').extract()
