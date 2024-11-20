import scrapy
from scrapy_splash import SplashRequest
import json

class LookerSpider(scrapy.Spider):
    name = 'lookers'
    
    # Define your Lua script
    lua_script = """
    function main(splash, args)
    splash:set_user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36")
    
    splash:on_request(function(request)
        request:set_header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
        request:set_header("Accept-Language", "en-US,en;q=0.5")
        request:set_header("Referer", "https://www.google.com")
        request:set_header("Upgrade-Insecure-Requests", "1")
    end)

    -- Load the page and wait for initial content
    assert(splash:go(args.url))
    assert(splash:wait(5))

    -- Scroll to the bottom to ensure lazy-loaded content appears
    splash:runjs("window.scrollTo(0, document.body.scrollHeight)")
    assert(splash:wait(3))

    -- Scroll back up if needed
    splash:runjs("window.scrollTo(0, 0)")
    assert(splash:wait(2))

    -- Click cookie consent button if present
    local cookie_button = splash:select('#cookie-accept')
    if cookie_button then
        cookie_button:mouse_click()
        assert(splash:wait(2))
    end

    -- Optionally, click other elements like "Load More"
    local load_more_button = splash:select('#load-more-button')
    if load_more_button then
        load_more_button:mouse_click()
        assert(splash:wait(3))
    end

    return {
        url = splash:url(),
        html = splash:html(),
    }
end
    """
    

# Start with the AJAX URL
    start_urls = [
        'https://api.lookers.co.uk/vehiclesearch/vehicle/search?Group=d90377b7-3fdf-460c-8090-10cf0207b7b4&Type=Car&condition=Dealer%20New%2C%20Nearly%20New%2CUsed&ignoreFacet=condition&skip=0&sortGroup=d90377b7-3fdf-460c-8090-10cf0207b7b4&sortOrder=Recommended&srsltid=AfmBOopLXJJMuc30je3HW7swmdHe5qYWNhIPeG1gw7RzM26fQZmZYyQE&take=24'
    ]

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

            # Yield a request to scrape the car details
            yield SplashRequest(
                url=car_url,
                method="GET",
                callback=self.parse_car,
                endpoint="execute",
                args={'lua_source': self.lua_script},
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
        
        # Handle pagination
        if offset < total_matches:
            next_url = f"https://api.lookers.co.uk/vehiclesearch/vehicle/search?Group=d90377b7-3fdf-460c-8090-10cf0207b7b4&Type=Car&condition=Dealer%20New%2C%20Nearly%20New%2CUsed&ignoreFacet=condition&skip={offset}&sortGroup=d90377b7-3fdf-460c-8090-10cf0207b7b4&sortOrder=Recommended&srsltid=AfmBOopLXJJMuc30je3HW7swmdHe5qYWNhIPeG1gw7RzM26fQZmZYyQE&take=24"
            yield scrapy.Request(url=next_url, callback=self.parse)

    def parse_car(self, response):
        # Extract car details passed via meta
        car_meta = response.meta

        # Extract additional car details from the detailed page
        car_info = response.xpath("//div[contains(@class, 'used-specs__data-col')]").css('span.used-specs__vehicle-data::text').getall()
        
        mpg = car_info[3] 
        previous_owners = car_info[5] 
        n_doors = car_info[7] 
        droplet = car_info[9]

        feature_list = []
        feature_panel = response.css('ul.feature-panel__ul')
        for item in feature_panel:
            items = [text.strip() for text in item.css('li::text').getall()]
            feature_list.extend(items)

        # Combine meta and scraped data
        car_data =  {
            **car_meta,
            "mpg": mpg,
            "previous_owners": previous_owners,
            "n_doors": n_doors,
            "droplet": droplet,
            "feature_list": feature_list,
        }
        
        car_data.pop('splash', None)
        
        yield car_data
