import scrapy
from scrapy_splash import SplashRequest


class CwspiderSpider(scrapy.Spider):
    name = "cwspider"
    allowed_domains = ["carwow.co.uk"]
    start_urls = ["https://quotes.carwow.co.uk/deals/f62828769e457ac19ebb1149421f5845"]
    #start_urls = ["https://www.carwow.co.uk/used-cars"]

    # def start_requests(self):
    #     # Use SplashRequest to dynamically load the page with JavaScript
    #     for url in self.start_urls:
    #         yield SplashRequest(url, self.parse, args={'wait': 1})


    def parse(self, response):

        cars = response.css('article.card-generic')
        for car in cars:
            url = car.css('a::attr(href)').get()
            yield{
                'url': url,
            }
        print(cars)
        
        car_name = response.css('span.deal-title__model::text').get()
        price = response.css('div.deal-pricing__carwow-price::text').get()
        
        yield{
            'car_name': car_name,
            'price': price,
        }

        details = response.css('div.summary-list__item')

        for div in details:
            title = div.css('dt::text').get()
            detail = div.css('dd::text').get()        

            yield{
                'title': title,
                'detail': detail,
            }

        