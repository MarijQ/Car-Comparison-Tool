import scrapy
from scrapy_splash import SplashRequest

class ExampleSpider(scrapy.Spider):
    name = "example_splash"

    def start_requests(self):
        url = 'http://quotes.toscrape.com/js'  # A page with dynamic JS-rendered quotes
        yield SplashRequest(url, self.parse, args={'wait': 2})

    def parse(self, response):
        quotes = response.css('div.quote span.text::text').getall()
        for quote in quotes:
            yield {'quote': quote}
