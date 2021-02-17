import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from banquehavilland.items import Article


class BanqueSpider(scrapy.Spider):
    name = 'banque'
    start_urls = ['https://www.banquehavilland.com/en/news']

    def parse(self, response):
        links = response.xpath('//ul[@class="list3 vanilla"]//li/a/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h1/text()').get()
        if title:
            title = title.strip()

        date = response.xpath('//time/text()').get()
        if date:
            date = datetime.strptime(date.strip(), '%d-%m-%Y')
            date = date.strftime('%Y/%m/%d')

        content = response.xpath('//section[@class="newsdetailsection"]//p//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
