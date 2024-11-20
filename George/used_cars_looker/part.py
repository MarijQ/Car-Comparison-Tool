class LookerSpider(scrapy.Spider):
    name = 'lookers'

    # Start URLs
    start_urls = [
        'https://api.lookers.co.uk/vehiclesearch/vehicle/search?Group=d90377b7-3fdf-460c-8090-10cf0207b7b4&Type=Car&condition=Dealer%20New%2C%20Nearly%20New%2CUsed&ignoreFacet=condition&skip=0&sortGroup=d90377b7-3fdf-460c-8090-10cf0207b7b4&sortOrder=Recommended&srsltid=AfmBOopLXJJMuc30je3HW7swmdHe5qYWNhIPeG1gw7RzM26fQZmZYyQE&take=24'
    ]

    def parse(self, response):
        # Parse the JSON response
        data = json.loads(response.text)
        
        
        
        cars_urls_list = []
        # Extract car details
        for car in data.get('Results', []): 
            car_name =  car.get('Make').lower().replace(" ", "-")
            car_model =  car.get('Model').lower().replace(" ", "-")
            car_id = car.get('Id')
            
            
            car_url = f'https://www.lookers.co.uk/used-car/{car_name}/{car_model}/id/{car_id}'
            
            cars_urls_list.append(car_url)
            
            yield {
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

            
            
        total_matches = data.get('Matches', 0)
        offset = data.get('Offset', 0) + len(data.get('Results', []))
        if offset < total_matches:
            next_url = f"https://api.lookers.co.uk/vehiclesearch/vehicle/search?Group=d90377b7-3fdf-460c-8090-10cf0207b7b4&Type=Car&condition=Dealer%20New%2C%20Nearly%20New%2CUsed&ignoreFacet=condition&skip={offset}&sortGroup=d90377b7-3fdf-460c-8090-10cf0207b7b4&sortOrder=Recommended&srsltid=AfmBOopLXJJMuc30je3HW7swmdHe5qYWNhIPeG1gw7RzM26fQZmZYyQE&take=24"
            yield scrapy.Request(url=next_url, callback=self.parse)