import scrapy
from scrapy.http import HtmlResponse
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class CargiantSpider(scrapy.Spider):
    name = "cargiant"
    start_urls = ['https://www.cargiant.co.uk/search/all/all']

    def parse(self, response):
        for page_num in range(5):  # Iterate over the first 5 pages
            logging.info(f"Processing page {page_num + 1}")

            # Wait for listings to load
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-vehicle]'))
                )
            except Exception as e:
                self.logger.error(f"Error loading listings: {e}")
                break

            # Get current HTML source
            body = self.driver.page_source
            response_obj = HtmlResponse(
                url=self.driver.current_url,
                body=body,
                encoding='utf-8',
            )

            # Process car listings
            listings = response_obj.css('div[data-vehicle]')
            if not listings:
                self.logger.warning("No listings found!")

            # Scrape individual listings
            for listing in listings:
                name = listing.css('span.title__main.set-h3::text').get()
                variant = listing.css('span.title__sub.set-h4::text').get()
                plate = listing.css('span.title__sub__plate::text').get()
                details = listing.css('span.text-content::text').get()
                price = listing.css('div.price-block__price::text').get()

                if name and price:
                    yield {
                        'name': name.strip(),
                        'variant': variant.strip() if variant else None,
                        'plate': plate.strip().lstrip(', ') if plate else None,
                        'details': details.strip() if details else None,
                        'price': price.strip()[4:],  # Strip currency symbol
                    }
                else:
                    self.logger.warning("Missing name or price in a listing.")

            # Check if the "Next" button exists and is clickable
            try:
                next_button = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, 'a.paging__item--next:not([disabled])'))
                )

                # Click the "Next" button to load the next page
                next_button.click()
                time.sleep(2)  # Short delay to allow page to load
            except Exception as e:
                self.logger.error(f"Error clicking next button: {e}")
                break
