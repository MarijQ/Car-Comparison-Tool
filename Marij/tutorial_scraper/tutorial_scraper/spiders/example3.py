import scrapy

class ExampleSpider(scrapy.Spider):
    name = "example3"
    start_urls = [
        'http://quotes.toscrape.com/'
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('span small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }

        # Follow the pagination link to scrape multiple pages
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            # Follow the link to the next page
            yield response.follow(next_page, self.parse)
