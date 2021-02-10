import scrapy

from scrapy.loader import ItemLoader
from ..items import BiverbancaItem
from itemloaders.processors import TakeFirst


class BiverbancaSpider(scrapy.Spider):
	name = 'biverbanca'
	start_urls = ['https://www.biverbanca.it/corporate-news/']

	def parse(self, response):
		post_links = response.xpath('//h2/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@rel="next"]/@href').getall()
		yield from response.follow_all(next_page, self.parse)


	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="entry-content"]//text()[normalize-space()]|//div[@class="et_pb_text_inner"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//article/div[@class="et_post_meta_wrapper"][1]/text()[normalize-space()]').get()

		item = ItemLoader(item=BiverbancaItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
