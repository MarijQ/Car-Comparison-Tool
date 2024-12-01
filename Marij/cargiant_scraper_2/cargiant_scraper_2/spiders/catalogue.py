import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.http import HtmlResponse
import logging
import time

class CargiantSpider(scrapy.Spider):
    name = "catalogue"
    start_urls = ['https://www.cargiant.co.uk/search/all/all']

    def __init__(self, *args, **kwargs):
        super(CargiantSpider, self).__init__(*args, **kwargs)
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Run in headless mode
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(options=chrome_options)
    
    def parse(self, response):
        self.driver.get(response.url)

        for page_num in range(5):  # change number of pages
            self.logger.info(f"Processing page {page_num + 1}")
            
            # Wait for the listings to load
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-vehicle]'))
                )
            except Exception as e:
                self.logger.error(f"Error loading listings: {e}")
                break

            # Grab the current HTML source
            body = self.driver.page_source
            response_obj = HtmlResponse(
                url=self.driver.current_url,
                body=body,
                encoding='utf-8',
            )

            # Parse car listing links
            listings = response_obj.css('a.car-listing-item__details')
            if not listings:
                self.logger.warning("No listings found!")

            for listing in listings:
                car_url = listing.attrib.get('href')
                if car_url:
                    # Construct the absolute URL
                    full_url = f"https://www.cargiant.co.uk{car_url}"
                    yield {
                        'url': full_url,
                    }
                else:
                    self.logger.warning("No URL found in a listing.")
            
            # Handle pagination by clicking the "Next" button
            try:
                next_button = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'a.paging__item--next'))
                )
                self.driver.execute_script("arguments[0].click();", next_button)
                time.sleep(2)  # Allow time for the next page to load
            except Exception as e:
                self.logger.error(f"Error clicking next button: {e}")
                break

    def closed(self, reason):
        self.driver.quit()
