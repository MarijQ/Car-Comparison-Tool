import scrapy
from scrapy_splash import SplashRequest
import json
from scrapy_used_cars.pipelines import CargiantFinalPipeline


class LookerSpider(scrapy.Spider):
    name = 'lookers'

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

    # Start with the API URL
    start_urls = [
        'https://api.lookers.co.uk/vehiclesearch/vehicle/search?Group=d90377b7-3fdf-460c-8090-10cf0207b7b4&Type=Car&condition=Dealer%20New%2C%20Nearly%20New%2CUsed&ignoreFacet=condition&skip=0&sortGroup=d90377b7-3fdf-460c-8090-10cf0207b7b4&sortOrder=Recommended&take=24'
    ]

    def parse(self, response):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Referer": "https://www.lookers.co.uk",
        }

        # Make a new request with these headers
        yield scrapy.Request(
            url=self.start_urls[0],
            callback=self.parse_json,
            headers=headers,
            dont_filter=True,
        )

    def parse_json(self, response):
        # Move the JSON parsing and pagination to this function
        data = json.loads(response.text)
        total_matches = data.get("Matches", 0)
        offset = data.get("Offset", 0) + len(data.get("Results", []))

        for car in data.get("Results", []):
            # Existing car URL and meta configuration logic remains unchanged
            car_name = car.get('Make').lower().replace(" ", "-")
            car_model = car.get('Model').lower().replace(" ", "-")
            car_id = car.get('Id')

            car_url = f"https://www.lookers.co.uk/used-car/{car_name}/{car_model}/id/{car_id}"

            yield SplashRequest(
                url=car_url,
                callback=self.parse_car,
                endpoint="execute",
                args={'lua_source': self.lua_script},
                meta={
                    "id": car.get("Id"),
                    "price": car.get("Price"),
                    # Add other metadata
                },
            )

        # Pagination (if more results exist)
        if offset < total_matches:
            next_offset = offset + 24
            next_url = self.start_urls[0].replace("skip=0", f"skip={next_offset}")
            yield scrapy.Request(url=next_url, callback=self.parse_json, headers=headers, dont_filter=True)


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
