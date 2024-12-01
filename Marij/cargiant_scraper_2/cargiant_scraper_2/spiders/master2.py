import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from scrapy.http import HtmlResponse
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import logging

class MasterSpider(scrapy.Spider):
    name = "master2"
    start_urls = ['https://www.cargiant.co.uk/search/all/all']

    def __init__(self, *args, **kwargs):
        super(MasterSpider, self).__init__(*args, **kwargs)
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Run in headless mode
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(options=chrome_options)

    def parse(self, response):
        self.driver.get(response.url)


        for page_num in range(3):  # Change this number to the desired number of pages
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

            for listing in listings[:2]:
                car_url = listing.attrib.get('href')
                if car_url:
                    # Construct the absolute URL
                    full_url = f"https://www.cargiant.co.uk{car_url}"
                    yield scrapy.Request(url=full_url, callback=self.parse_listing)
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

    def parse_listing(self, response):
        self.logger.info(f"Processing next listing ...")
        self.driver.get(response.url)
        time.sleep(0.2)  # Wait for the page to load

        # Initialize dictionary for output
        output = {}
        output["url"] = response.url

        # Extract the title which includes both brand and model
        try:
            title_element = self.driver.find_element(By.CSS_SELECTOR, 'h1.title__main.set-h3')
            title = title_element.text.strip()
            title_parts = title.split(None, 1)  # Split into brand and model
            output["brand"] = title_parts[0]
            output["model"] = title_parts[1] if len(title_parts) > 1 else None
        except Exception as e:
            self.logger.error(f"Error extracting title: {e}")
            output["brand"] = None
            output["model"] = None

        # Extract price from top part
        try:
            price_element = self.driver.find_element(By.CSS_SELECTOR, 'div.price-block__price')
            price = price_element.text.strip()
            output["Price"] = price.replace('£', '').replace(',', '').strip()
        except Exception as e:
            self.logger.error(f"Error extracting price: {e}")
            output["Price"] = None

        # Collect all items from details section on page
        details = {}
        try:
            items = self.driver.find_elements(By.CSS_SELECTOR, 'li.details-panel-item__list__item')
            for item in items:
                spans = item.find_elements(By.CSS_SELECTOR, 'span')
                if len(spans) >= 2:
                    key = spans[0].text.strip()
                    value = spans[1].text.strip()
                    details[key] = value
        except Exception as e:
            self.logger.error(f"Error extracting details: {e}")

        # Extract the required metrics from the details dictionary
        output["Year"] = details.get('Year')
        output["Mileage"] = details.get('Mileage')
        output["Fuel"] = details.get('Fuel Type')
        output["Transmission"] = details.get('Transmission')
        output["Body"] = details.get('Body Type')

        # Click on the Performance tab to extract additional data
        try:
            # Wait until the Performance tab is clickable and click it
            performance_tab = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.tab-wrap__head__inner__tabs__tab[data-tab="tab1"]'))
            )
            performance_tab.click()
            time.sleep(0.2)  # Wait for the Performance tab to load

            # Extract CC and Engine Power BHP from the Performance tab
            cc = None
            bhp = None
            rows = self.driver.find_elements(By.CSS_SELECTOR, 'div#tab1 table.specs-table tr')
            for row in rows:
                try:
                    th = row.find_element(By.CSS_SELECTOR, 'th').text.strip()
                    td = row.find_element(By.CSS_SELECTOR, 'td').text.strip()
                    if th == 'CC':
                        cc = td
                    elif th == 'Engine Power - BHP':
                        bhp = td
                except Exception as e:
                    self.logger.error(f"Error extracting Performance data: {e}")
                    continue

            # Convert CC to litres
            if cc:
                try:
                    output["litres"] = str(float(cc.replace(',', '')) / 1000)  # Convert to litres
                except ValueError:
                    output["litres"] = None
            else:
                output["litres"] = None

            # Store BHP
            output["hp"] = bhp if bhp else None
        except Exception as e:
            self.logger.error(f"Error clicking Performance tab or extracting data: {e}")
            output["litres"] = None
            output["hp"] = None

        # Yield the output as an item
        yield output

    def closed(self, reason):
        self.driver.quit()
