import scrapy
import time
class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ['http://quotes.toscrape.com/tag/humor/']


    def parse(self, response):
        time.sleep(15)
        print(f'in spider {self.name}')
        for quote in response.css('div.quote'):
            print(quote.css('span.text::text').extract_first())

    def close(self,reason):
        print('===================== spider close ================')

class QuotesSpider1(scrapy.Spider):
    name = "quotes_1"
    start_urls = ['http://quotes.toscrape.com/tag/humor/']

    def parse(self, response):
        print('meta content ==============')
        print(response.meta)
        print('meta content ==============')

        print(f'in spider {self.name}')
        for quote in response.css('div.quote'):
            print(quote.css('span.text::text').extract_first())

    def close(self,reason):
        print('===================== spider close ================')
