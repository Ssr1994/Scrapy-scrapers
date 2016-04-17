# -*- coding: utf-8 -*-
import scrapy
from tencentAC.items import TencentChap

class TencentSpider(scrapy.Spider):
    name = "tencent"
    allowed_domains = ["qq.com"]
    start_urls = (
        'http://ac.qq.com/Comic/comicInfo/id/524126',
    )

    def parse(self, response):
        cnt = 0
        for a in response.xpath('//ol[@class="chapter-page-all works-chapter-list"]//a'):
            if cnt >= 1:
                break
            cnt = cnt + 1
            href = a.xpath('@href')[0].extract()
            title = a.xpath('text()').extract()
            yield scrapy.Request(response.urljoin(href), callback=self.parse_content, 
                                 meta={"phantomjs":True, "title":title})
    
    def parse_content(self, response):
        chap = TencentChap()
        chap["title"] = response.meta["title"];
        chap['image_urls'] = [src for src in response.xpath('//ul[@class="comic-contain"]//img/@src').extract()]
        yield chap
    