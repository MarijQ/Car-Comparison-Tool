import scrapy
from scrapy_splash import SplashRequest
import json
import random
from scrapy.utils.project import get_project_settings


class LookerSpider(scrapy.Spider):
    name = 'lookers'

    def __init__(self, *args, **kwargs):
        super(LookerSpider, self).__init__(*args, **kwargs)
        
        # Get the current project settings
        settings = get_project_settings()
        
        # Set the settings for this spider from the custom settings module
        settings.setmodule('myproject.settings.cargiant_settings', priority='project')
        
    # Define your Lua script for Splash
    lua_script = """
        function main(splash, args)
            -- Set a realistic User-Agent (browser-like)
            splash:set_user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36")

            -- Clear cookies to start fresh
            splash:clear_cookies()

            -- Add necessary HTTP headers
            splash:on_request(function(request)
                request:set_header("Accept", "application/json, text/plain, */*")
                request:set_header("Accept-Language", "en-US,en;q=0.9")
                request:set_header("Referer", "https://www.lookers.co.uk")
                request:set_header("Connection", "keep-alive")
            end)

            -- Navigate to the URL
            assert(splash:go(args.url))

            -- Wait to allow the page to load
            assert(splash:wait(3))

            -- Return the final rendered HTML and cookies (to debug further)
            return {
                url = splash:url(),
                cookies = splash:get_cookies(),
                html = splash:html()
            }
        end
    """

# Start with the AJAX URL
    start_urls = [
        'https://api.lookers.co.uk/vehiclesearch/vehicle/search?Group=d90377b7-3fdf-460c-8090-10cf0207b7b4&Type=Car&condition=Dealer%20New%2C%20Nearly%20New%2CUsed&ignoreFacet=condition&skip=0&sortGroup=d90377b7-3fdf-460c-8090-10cf0207b7b4&sortOrder=Recommended&srsltid=AfmBOopLXJJMuc30je3HW7swmdHe5qYWNhIPeG1gw7RzM26fQZmZYyQE&take=24'
    ]
    
    def get_splash_url(self):
        return random.choice(self.settings.get('SPLASH_URLS'))

    def parse(self, response):
        # Parse the JSON response
        data = json.loads(response.text)
        total_matches = data.get('Matches', 0)
        offset = data.get('Offset', 0) + len(data.get('Results', []))

        # Generate car-specific URLs and yield requests
        for car in data.get('Results', []):
            car_name = car.get('Make').lower().replace(" ", "-")
            car_model = car.get('Model').lower().replace(" ", "-")
            car_id = car.get('Id')
            
            car_url = f'https://www.lookers.co.uk/used-car/{car_name}/{car_model}/id/{car_id}'
            
            splash_url = self.get_splash_url()
            # Yield a request to scrape the car details
            yield SplashRequest(
                url=car_url,
                method="GET",
                callback=self.parse_car,
                endpoint="execute",
                args={'lua_source': self.lua_script},
                splash_url=splash_url,
                splash_headers={'Content-Type': 'application/json'},
                meta={
                    "id": car.get("Id"),
                    "price": car.get("Price"),
                    "make": car.get("Make"),
                    "model": car.get("Model"),
                    "mileage": car.get("Odometer"),
                    "fuel_type": car.get("FuelType"),
                    "body_style": car.get("BodyStyle"),
                    "engine_size": car.get("EngineSize"),
                    "transmission": car.get("Transmission"),
                    "year": car.get("ModelYear"),
                    "dealership_name": car.get("DealershipName"),
                    "registered_date": car.get("RegisteredDate"),
                }
            )
        
        # Handle pagination (get the next's page ajax)
        if offset < total_matches:
            next_url = f"https://api.lookers.co.uk/vehiclesearch/vehicle/search?Group=d90377b7-3fdf-460c-8090-10cf0207b7b4&Type=Car&condition=Dealer%20New%2C%20Nearly%20New%2CUsed&ignoreFacet=condition&skip={offset}&sortGroup=d90377b7-3fdf-460c-8090-10cf0207b7b4&sortOrder=Recommended&srsltid=AfmBOopLXJJMuc30je3HW7swmdHe5qYWNhIPeG1gw7RzM26fQZmZYyQE&take=24"
            yield scrapy.Request(url=next_url, callback=self.parse)


    def parse_car(self, response):
        # Extract car details passed via meta
        car_meta = response.meta

        # Extract additional car details from the detailed page
        car_info = response.xpath("//div[contains(@class, 'used-specs__data-col')]").css('span.used-specs__vehicle-data::text').getall()

        # Handle missing data for MPG, number of doors, previous owners, etc.
        mpg, previous_owners, n_doors, droplet = None, None, None, None
        if len(car_info) >= 8:
            mpg = car_info[3] if len(car_info) > 3 else None
            previous_owners = car_info[5] if len(car_info) > 5 else None
            n_doors = car_info[7] if len(car_info) > 7 else None
            droplet = car_info[9] if len(car_info) > 9 else None

        # Extract feature list
        feature_list = []
        feature_panel = response.css('ul.feature-panel__ul')
        for item in feature_panel:
            features = [text.strip() for text in item.css('li::text').getall()]
            feature_list.extend(features)

        # Create item dictionary compatible with `car_db` schema
        car_item = {
            "make": car_meta.get("make"),
            "model": car_meta.get("model"),
            "price": car_meta.get("price"),
            "mileage": car_meta.get("mileage"),
            "fuel_type": car_meta.get("fuel_type"),
            "body_style": car_meta.get("body_style"),
            "engine_size": car_meta.get("engine_size"),
            "transmission": car_meta.get("transmission"),
            "year": car_meta.get("year"),
            "dealership_name": car_meta.get("dealership_name"),
            "mpg": mpg,
            "n_doors": n_doors,
            "previous_owners": previous_owners,
            "droplet": droplet,
            "feature_list": ", ".join(feature_list),
        }

        # Yield the item to the pipeline
        yield car_item
