import psycopg2
from datetime import datetime


class CargiantFinalPipeline:
    def open_spider(self, spider):
        # Connect to PostgreSQL when the spider opens
        self.connection = psycopg2.connect(
            dbname="used_cars",
            user="marij",
            password="marij", 
            host="localhost",
        )
        self.cursor = self.connection.cursor()

    def close_spider(self, spider):
        # Close the database connection
        self.cursor.close()
        self.connection.close()

    def process_item(self, item, spider):
        # Insert or update the car listing
        try:
            self.cursor.execute(
                """
                INSERT INTO car_listings (
                    url, brand, model, price, year, mileage,
                    fuel, transmission, body, litres, hp, last_updated
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (url) DO UPDATE SET
                    brand = EXCLUDED.brand,
                    model = EXCLUDED.model,
                    price = EXCLUDED.price,
                    year = EXCLUDED.year,
                    mileage = EXCLUDED.mileage,
                    fuel = EXCLUDED.fuel,
                    transmission = EXCLUDED.transmission,
                    body = EXCLUDED.body,
                    litres = EXCLUDED.litres,
                    hp = EXCLUDED.hp,
                    last_updated = CURRENT_TIMESTAMP;
            """,
                (
                    item.get("url"),
                    item.get("brand"),
                    item.get("model"),
                    float(item.get("Price")) if item.get("Price") else None,
                    int(item.get("Year")) if item.get("Year") else None,
                    item.get("Mileage"),
                    item.get("Fuel"),
                    item.get("Transmission"),
                    item.get("Body"),
                    float(item.get("litres")) if item.get("litres") else None,
                    float(item.get("hp")) if item.get("hp") else None,
                    datetime.now(),
                ),
            )
            self.connection.commit()
        except Exception as e:
            spider.logger.error(f"Database insertion error: {e}")
            self.connection.rollback()
        return item
