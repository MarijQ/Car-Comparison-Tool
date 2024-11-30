import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.http import HtmlResponse
import json
import os
import time
import subprocess
import sys

class CargiantSpider(scrapy.Spider):
    name = "master"
    start_urls = ['https://www.cargiant.co.uk/search/all/all']

    def __init__(self, *args, **kwargs):
        super(CargiantSpider, self).__init__(*args, **kwargs)
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Run in headless mode
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(options=chrome_options)
        self.urls_file = "urls.json"
        self.results_file = "results.json"

        # Delete old files if they exist
        if os.path.exists(self.urls_file):
            os.remove(self.urls_file)
        if os.path.exists(self.results_file):
            os.remove(self.results_file)

    def parse(self, response):
        self.driver.get(response.url)

        all_urls = []  # Save all the car listing URLs

        for page_num in range(1):  # Adjust number of pages as needed
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
                    all_urls.append(full_url)
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

        # Save all URLS to urls.json
        self.logger.info(f"Found {len(all_urls)} URLs in total.")
        self.save_urls_to_json(all_urls)

        # Call the individual listing spider for each URL
        self.crawl_ind_listing(all_urls)

    def save_urls_to_json(self, urls):
        """Save all collected URLs to a JSON file."""
        try:
            with open(self.urls_file, 'w') as f:
                json.dump(urls, f, indent=2)
            self.logger.info(f"Saved {len(urls)} URLs to {self.urls_file}.")
        except Exception as e:
            self.logger.error(f"Error saving URLs to file: {e}")

    def crawl_ind_listing(self, urls):
        """Run the 'ind_listing' spider once with all URLs."""
        # Write all URLs to a temporary file
        temp_urls_file = 'temp_urls.json'
        with open(temp_urls_file, 'w') as f:
            json.dump(urls, f)

        try:
            # Get the project root directory (where scrapy.cfg is located)
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.logger.info(f"Using project root directory: {project_root}")

            # Update PYTHONPATH in the environment variables
            env = os.environ.copy()
            env['PYTHONPATH'] = project_root + os.pathsep + env.get('PYTHONPATH', '')

            # Use sys.executable to ensure the subprocess uses the same Python environment
            subprocess.run(
                [
                    sys.executable, "-m", "scrapy", "crawl", "ind_listing",
                    "-a", f"urls_file={temp_urls_file}",
                    "-o", self.results_file,
                    "-t", "json"
                ],
                check=True,
                cwd=project_root,  # Set the working directory to project root
                env=env  # Pass the updated environment variables
            )
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error while running ind_listing spider: {e}")

    def closed(self, reason):
        self.driver.quit()
