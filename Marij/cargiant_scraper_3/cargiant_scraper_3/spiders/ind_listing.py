import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json
import logging
import time

class CargiantSpider(scrapy.Spider):
    name = 'ind_listing'

    def __init__(self, *args, **kwargs):
        super(CargiantSpider, self).__init__(*args, **kwargs)
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Run in headless mode
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(options=chrome_options)

        # Read URLs from the passed file
        urls_file = kwargs.get('urls_file')
        if urls_file:
            self.logger.info(f"Reading URLs from file: {urls_file}")
            with open(urls_file, 'r') as f:
                self.start_urls = json.load(f)
            self.logger.info(f"Loaded {len(self.start_urls)} URLs.")
        else:
            self.logger.error("No URLs file provided!")
            self.start_urls = []

    def start_requests(self):
        # Log that start_requests is invoked
        self.logger.info("Starting to process URLs...")
        for url in self.start_urls:
            self.logger.info(f"Processing URL: {url}")
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        self.driver.get(response.url)
        time.sleep(1)  # Wait for the page to load

        # Initialize dictionary for output
        output = {"url": response.url}

        # Extract title
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

        # Log the parsed output
        self.logger.info(f"Scraped data: {output}")

        yield output

    def closed(self, reason):
        self.driver.quit()
