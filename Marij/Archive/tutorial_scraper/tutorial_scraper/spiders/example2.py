import scrapy

class ExampleSpider(scrapy.Spider):
    # Name your spider
    name = "example2"

    # Start crawling from this URL
    start_urls = [
        'http://quotes.toscrape.com/'  # This is a simple demo site for scraping practice
    ]

    def parse(self, response):
        # Extract data using XPath or CSS selectors
        quotes = response.css('div.quote span.text::text').getall()

        # Display data to the console
        for quote in quotes:
            yield {'quote': quote}
