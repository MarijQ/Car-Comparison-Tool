import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from scrapy.http import HtmlResponse
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import logging
from scrapy.exceptions import CloseSpider


class MasterSpider(scrapy.Spider):
    name = "master3"
    start_urls = ['https://www.cargiant.co.uk/search/all/all']
    custom_settings = {
        "CONCURRENT_REQUESTS": 16,
        "RETRY_ENABLED": True,
    }

    def __init__(self, *args, **kwargs):
        super(MasterSpider, self).__init__(*args, **kwargs)
        self.collected_urls = []  # Collect all URLs here in phase 1
        # self.logger = logging.getLogger(__name__)

        # Selenium WebDriver setup
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Run browser in headless mode
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(options=chrome_options)

    def parse(self, response):
        """
        Phase 1: Use Selenium to collect all listing URLs from pagination.
        """
        self.logger.info("Starting phase 1: Collecting listing URLs.")
        self.driver.get(response.url)

        while True:
            # Wait for the listings to load
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-vehicle]'))
                )
                self.logger.info(f"Page loaded: {self.driver.current_url}")
            except TimeoutException:
                self.logger.error("Timeout while waiting for listings. Stopping.")
                break

            # Grab the current HTML and extract listings
            body = self.driver.page_source
            current_response = HtmlResponse(
                url=self.driver.current_url,
                body=body,
                encoding='utf-8',
            )
            listings = current_response.css('a.car-listing-item__details::attr(href)').extract()
            absolute_urls = [f"https://www.cargiant.co.uk{url}" for url in listings]
            self.collected_urls.extend(absolute_urls)
            self.logger.info(f"Collected {len(absolute_urls)} URLs from this page.")

            # Try to navigate to the next page
            try:
                next_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.paging__item--next'))
                )
                self.driver.execute_script("arguments[0].click();", next_button)
            except TimeoutException:
                self.logger.info("No more pages to navigate. Exiting phase 1.")
                break

        # After collecting all URLs, move to phase 2
        if not self.collected_urls:
            self.logger.error("No URLs found during phase 1.")
            raise CloseSpider("No listings to scrape.")

        self.logger.info(f"Collected a total of {len(self.collected_urls)} listing URLs.")
        for url in self.collected_urls:
            yield scrapy.Request(url=url, callback=self.parse_listing)

        # Close the driver after Phase 1
        self.driver.quit()

    def parse_listing(self, response):
        """
        Phase 2: Use Scrapy to parse individual listing pages for details.
        """
        self.logger.info(f"Scraping details from {response.url}")

        output = {}
        output["url"] = response.url

        # Extract the title (brand and model)
        title = response.css('h1.title__main.set-h3::text').get()
        if title:
            title_parts = title.strip().split(None, 1)
            output["brand"] = title_parts[0]
            output["model"] = title_parts[1] if len(title_parts) > 1 else None
        else:
            output["brand"] = None
            output["model"] = None

        # Extract price
        price = response.css('div.price-block__price::text').get()
        output["Price"] = price.replace('£', '').replace(',', '').strip() if price else None

        # Extract details section
        details = {}
        for item in response.css('li.details-panel-item__list__item'):
            key = item.css('span:nth-child(1)::text').get()
            value = item.css('span:nth-child(2)::text').get()
            if key and value:
                details[key.strip()] = value.strip()

        output["Year"] = details.get('Year')
        output["Mileage"] = details.get('Mileage')
        output["Fuel"] = details.get('Fuel Type')
        output["Transmission"] = details.get('Transmission')
        output["Body"] = details.get('Body Type')

        # Extract Performance tab data
        cc = response.xpath("//th[text()='CC']/following-sibling::td/text()").get()
        bhp = response.xpath("//th[text()='Engine Power - BHP']/following-sibling::td/text()").get()

        # Convert CC to litres if available
        if cc:
            try:
                output["litres"] = str(float(cc.replace(',', '').strip()) / 1000) if cc else None
            except ValueError:
                output["litres"] = None
        else:
            output["litres"] = None

        # Store BHP
        output["hp"] = bhp if bhp else None

        yield output
