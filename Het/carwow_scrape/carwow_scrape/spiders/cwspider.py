import scrapy
from scrapy_splash import SplashRequest

class CarwowSpider(scrapy.Spider):
    name = "carwow"
    allowed_domains = ["carwow.co.uk"]
    start_urls = ["https://www.carwow.co.uk/used-cars"]

    base_url = "https://www.carwow.co.uk/used-cars?age=0%2C9&budget=0%2C150000&mileage=0%2C100000&stock_type=used&pagination%5Bcurrent_page%5D={page}&pagination%5Bper_page%5D=12"

    # Splash script for gradual scrolling
    scroll_script = """
    function main(splash, args)
        splash:go(args.url)
        splash:wait(2)
        local scroll_to = splash:jsfunc("window.scrollTo")
        local get_height = splash:jsfunc("document.body.scrollHeight")
        local height = 0
        local prev_height = -1
        while height ~= prev_height do
            prev_height = height
            height = get_height()
            for i = 1, 10 do
                scroll_to(0, height * i / 10)
                splash:wait(0.5)
            end
        end
        return splash:html()
    end
    """

    def start_requests(self):
        total_pages = 100  # Or dynamically determine total pages
        for page in range(1, total_pages + 1):
            yield SplashRequest(
                url=self.base_url.format(page=page),
                callback=self.parse,
                endpoint="execute",
                args={"lua_source": self.scroll_script},
            )

    def parse(self, response):
        cars = response.css('article.card-generic')
        for car in cars:
            link = car.css('div.card-generic__section div.card-generic__ctas a::attr(href)').get()
            if link:
                yield SplashRequest(
                    url=response.urljoin(link),
                    callback=self.parse_car_details,
                    endpoint="execute",
                    args={"lua_source": self.scroll_script},
                )

    def parse_car_details(self, response):
        car_name = response.css('span.deal-title__model::text').get(default="N/A")
        price = response.css('div.deal-pricing__carwow-price::text').get(default="N/A")
        details = response.css('div.summary-list__item')

        car_details = {
            "car_name": car_name,
            "price": price,
            "specifications": {}
        }

        for detail in details:
            title = detail.css('dt::text').get()
            value = detail.css('dd::text').get()
            if title and value:
                car_details["specifications"][title] = value

        yield car_details