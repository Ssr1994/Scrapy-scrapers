# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request

class TencentacPipeline(ImagesPipeline):
    
    def get_media_requests(self, item, info):
        return [Request(x, meta={"title":item["title"], "index":k}) for k, x in enumerate(item["image_urls"])]
    
    def file_path(self, request, response=None, info=None):
        return '%s/%s.jpg' % (request.meta["title"][0], request.meta["index"])
