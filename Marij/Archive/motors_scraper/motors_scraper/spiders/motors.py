import scrapy

class MotorsSpider(scrapy.Spider):
    name = "motors"
    start_urls = ['https://www.motors.co.uk/car-72642888/?i=16&m=sr']

    def parse(self, response):
        # Extract the brand and model from the h1 element
        title = response.css('h1.no-margin.no-scale.title-3::text').get()

        # Split the title into brand and model
        if title:
            brand, model = title.split(', ')
        else:
            brand, model = None, None

        car = {
            'brand': brand,
            'model': model,
            # Other fields can be added here
            'year': response.css('.car-year::text').get(),  # Example, add your selectors
            'litres': response.css('.engine-size::text').get(),  # Example
            'hp': response.css('.horsepower::text').get(),  # Example
            'miles': response.css('.mileage-text::text').get(),  # Example
            'fuel': response.css('.fuel-type::text').get(),  # Example
            'transmission': response.css('.transmission-type::text').get(),  # Example
            'body_style': response.css('.body-style::text').get(),  # Example
            'price': response.css('div.price::text').get(),  # Example
        }
        print(f"\n ----- \n {car} \n ----- \n")
