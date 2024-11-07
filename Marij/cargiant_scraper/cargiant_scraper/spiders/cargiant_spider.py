import scrapy
from scrapy_splash import SplashRequest

class CargiantSpider(scrapy.Spider):
    name = 'cargiant'
    start_urls = [
        'https://www.cargiant.co.uk/car/Toyota/Corolla/WK20VWW'
    ]

    def start_requests(self):
        # Use SplashRequest to dynamically load the page with JavaScript
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 1})

    def parse(self, response):
        # Initialise dictionary for output
        output = {}

        # Extract the title which includes both brand and model
        title = response.css('h1.title__main.set-h3::text').get()
        title_parts = title.strip().split(None, 1)  # Split into brand and model
        output["brand"] = title_parts[0]
        output["model"] = title_parts[1] if len(title_parts) > 1 else None

        # Extract price from top part
        price = response.css('div.price-block__price::text').get()
        output["Price"] = price.replace('£', '').replace(',', '').strip()

        # Collect all items from details section on page
        details = {}
        for item in response.css('li.details-panel-item__list__item'):
            key = item.css('span::text').get() # get first one
            value = item.css('span::text').getall()[1].strip() # get all and pick 2nd
            details[key] = value

        # Extract the required metrics from the details dictionary
        output["Year"] = details.get('Year')
        output["Mileage"] = details.get('Mileage')
        output["Fuel"] = details.get('Fuel Type')
        output["Transmission"] = details.get('Transmission')
        output["Body"] = details.get('Body Type')

        # Request the Performance tab dynamically through Splash
        performance_tab_url = response.urljoin("#tab1")
        yield SplashRequest(
            performance_tab_url,
            self.parse_performance,
            args={'wait': 1},
            meta={'output': output}  # Pass the current output down
        )

    def parse_performance(self, response):
        # Retrieve the output from meta
        output = response.meta.get('output', {})

        # Extract CC and Engine Power BHP from Performance tab
        cc = response.css("td:contains('CC') + td::text").get() # contains=looks for text, "+"=next adjacent element
        bhp = response.css("td:contains('Engine Power - BHP') + td::text").get()

        # Convert CC to litres
        if cc:
            output["litres"] = str(float(cc)/1000)  # Convert to litres

        # Store BHP
        output["hp"] = bhp.strip() if bhp else None

        # Output the final results
        self.print_dictionary(output)

    def print_dictionary(self, d):
        for key, value in d.items():
            print(f"{key}: {value}")
