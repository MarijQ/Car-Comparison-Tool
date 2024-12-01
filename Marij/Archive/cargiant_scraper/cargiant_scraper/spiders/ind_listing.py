import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

class CargiantSpider(scrapy.Spider):
    name = 'cargiant'
    start_urls = [
        'https://www.cargiant.co.uk/car/Toyota/Corolla/WK20VWW'
    ]

    def __init__(self, *args, **kwargs):
        super(CargiantSpider, self).__init__(*args, **kwargs)
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Run in headless mode
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(options=chrome_options)

    def parse(self, response):
        self.driver.get(response.url)
        time.sleep(3)  # Wait for the page to load

        # Initialize dictionary for output
        output = {}

        # Extract the title which includes both brand and model
        try:
            title_element = self.driver.find_element(By.CSS_SELECTOR, 'h1.title__main.set-h3')
            title = title_element.text.strip()
            title_parts = title.split(None, 1)  # Split into brand and model
            output["brand"] = title_parts[0]
            output["model"] = title_parts[1] if len(title_parts) > 1 else None
        except Exception:
            output["brand"] = None
            output["model"] = None

        # Extract price from top part
        try:
            price_element = self.driver.find_element(By.CSS_SELECTOR, 'div.price-block__price')
            price = price_element.text.strip()
            output["Price"] = price.replace('£', '').replace(',', '').strip()
        except Exception:
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
        except Exception:
            pass

        # Extract the required metrics from the details dictionary
        output["Year"] = details.get('Year')
        output["Mileage"] = details.get('Mileage')
        output["Fuel"] = details.get('Fuel Type')
        output["Transmission"] = details.get('Transmission')
        output["Body"] = details.get('Body Type')

        # Click on the Performance tab
        try:
            performance_tab = self.driver.find_element(By.CSS_SELECTOR, 'a[href="#tab1"]')
            performance_tab.click()
            time.sleep(2)  # Wait for the Performance tab to load

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
                except Exception:
                    continue

            # Convert CC to litres
            if cc:
                try:
                    output["litres"] = str(float(cc) / 1000)  # Convert to litres
                except ValueError:
                    output["litres"] = None
            else:
                output["litres"] = None

            # Store BHP
            output["hp"] = bhp if bhp else None
        except Exception:
            output["litres"] = None
            output["hp"] = None

        # Output the final results
        self.print_dictionary(output)

    def print_dictionary(self, d):
        for key, value in d.items():
            self.logger.info(f"{key}: {value}")

    def closed(self, reason):
        self.driver.quit()
