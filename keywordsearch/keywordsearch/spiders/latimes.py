# -*- coding: utf-8 -*-
import scrapy
import urllib
from keywordsearch.items import KeywordsearchItem
from keywordsearch.settings import QUERY, FILE_PATH

class LatimesSpider(scrapy.Spider):
	name = "latimes"
	orgname = "Los Angeles Times"
	allowed_domains = ['latimes.com']
	query_url = "http://www.latimes.com/search/dispatcher.front?Query="
	options = "&target=all&isSearch=true&spell=on"

	def start_requests(self):
		yield scrapy.Request(self.query_url + urllib.quote_plus(QUERY) + self.options, callback=self.parse)

	def parse(self, response):
		for url in response.xpath('//div[@class="trb_search_result_wrapper"]/a/@href').extract():
			yield scrapy.Request(response.urljoin(url), self.parse_article)

	def parse_article(self, response):
		item = KeywordsearchItem()
		item['title'] = response.xpath('//div[@class="trb_ar_hl"]/h1/text()').extract()
		if not item['title']:
			item['title'] = response.xpath('//div[@class="trb_article_title"]/h1/text()').extract()

		item['author'] = response.xpath('//span[@class="trb_ar_by_nm_au"]/a/text()').extract()
		if not item['author']:
			item['author'] = response.xpath('//span[@class="trb_bylines_nm_au"]/a/text()').extract()	
		if not item['author']:
			item['author'] = response.xpath('//span[@class="trb_ar_by_nm_au"]/span/text()').extract()

		item['time'] = response.xpath('//div[@class="trb_ar_dateline"]/time/@data-dt').extract()
		if not item['time']:
			item['time'] = response.xpath('//div[@class="trb_article_dateline"]/time/@data-dt').extract()
		
		item['publisher'] = self.orgname
		item['url'] = response.url

		item['content'] = ' '.join(response.xpath('//div[@class="trb_ar_page"]/p//text()').extract())
		if not item['content']:
			item['content'] = ' '.join(response.xpath('//div[@id="story"]/p//text()').extract())
		if not item['content']:
			item['content'] = ' '.join(response.xpath('//div[@id="liveblog-description"]/p//text()').extract())
		item['query'] = QUERY
		item['keyLine'] = ""
		with open(FILE_PATH + ''.join(item['title']).lstrip() + '.html', 'w') as f:
			f.write(response.body)
		yield item
