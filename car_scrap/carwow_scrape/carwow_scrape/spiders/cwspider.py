import scrapy
from scrapy_splash import SplashRequest


class CwspiderSpider(scrapy.Spider):
    name = "cwspider"
    allowed_domains = ["carwow.co.uk"]
    start_urls = ["https://www.carwow.co.uk/used-cars"]

    def start_requests(self):
        # Use SplashRequest to dynamically load the page with JavaScript
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 1})

    def parse(self, response):
        
        car_name = response.css('span.deal-title__model::text').get()
        price = response.css('td.div.card-generic__pricing::text').get()
        print(car_name)
        print(price)

    

 
        
        
