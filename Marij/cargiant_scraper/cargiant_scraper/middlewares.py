import logging
from selenium.webdriver.remote.remote_connection import LOGGER as selenium_logger
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set Selenium logging level to WARNING
selenium_logger.setLevel(logging.WARNING)

class SeleniumMiddleware:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def process_request(self, request, spider):
        logging.info(f"Processing URL: {request.url}")
        if not hasattr(spider, 'driver'):
            spider.driver = self.driver  # Attach driver to spider
        self.driver.get(request.url)

        # Wait for the listings to appear
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-vehicle]"))
            )
        except Exception as e:
            logging.error(f"Error: {e}")

        body = self.driver.page_source
        return HtmlResponse(
            url=self.driver.current_url,
            body=body,
            encoding='utf-8',
            request=request
        )

    def spider_closed(self):
        self.driver.quit()
