import scrapy
from scrapy_splash import SplashRequest

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

    # Start Requests
    def start_requests(self):
        

        url = 'https://www.lookers.co.uk/used-car/vauxhall/corsa/1-0-ecoflex-s-3dr/id/669019'
        yield SplashRequest(
            url=url,
            callback=self.parse_car,
            endpoint="execute",
            args={'lua_source': self.lua_script},
            splash_headers={'Content-Type': 'application/json'}
        )
    

    # Parse the Response
    def parse_car(self, response):
        
        
        vehicle_name = response.xpath("//div[contains(@class, 'vehicle-header__variant vehicle-header__desktop-only')]/text()").get().strip()
        vehicle_stats = response.xpath("//div[contains(@class, 'vehicle-header__stats vehicle-header__desktop-only')]/text()").get().strip()
    
        # car's price
        price = response.xpath("//div[contains(@class, 'vehicle-header__price--full-value')]//span/text()").get().strip()
        
        # car's information (miles, type of transimission etc)
        car_info = response.xpath("//div[contains(@class, 'used-specs__data-col')]").css('span.used-specs__vehicle-data::text').getall()
        
        
        miles = car_info[0]
        year = car_info[1]
        fuel = car_info[2]
        mpg = car_info[3]
        engine_size = car_info[4]
        previous_owners = car_info[5]
        transmission = car_info[6]
        n_doors = car_info[7]
        registration = car_info[8]
        droplet = car_info[9]
            
        
        # car's features list
        feature_list = []
        feature_panel = response.css('ul.feature-panel__ul')
        for item in feature_panel:
            items = [text.strip() for text in item.css('li::text').getall()]
            feature_list.extend(items)
            

        yield {
            "car_name": vehicle_name,
            "vehicle_stats": vehicle_stats,
            "price": price,
            "miles": miles,
            "model_year" : year,
            "fuel": fuel,
            "mpg": mpg,
            "engine_size": engine_size,
            "previous_owners": previous_owners,
            "transmission": transmission,
            "n_doors" : n_doors,
            "registration": registration,
            "droplet":droplet,
            "feature_list": feature_list,
        }
