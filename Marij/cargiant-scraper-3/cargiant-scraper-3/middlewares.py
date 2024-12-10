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
from scrapy import signals

# Suppress unnecessary Selenium logs
selenium_logger.setLevel(logging.WARNING)

class SeleniumMiddleware:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")  # Required for some environments
        chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls()
        crawler.signals.connect(middleware.spider_closed, signal=signals.spider_closed)
        return middleware

    def process_request(self, request, spider):
        logging.info(f"Processing URL: {request.url}")
        self.driver.get(request.url)

        try:
            # Wait until the target element is present
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-vehicle]"))
            )
        except Exception as e:
            logging.error(f"Error loading page {request.url}: {e}")
            return HtmlResponse(
                url=self.driver.current_url,
                status=500,
                request=request,
                body=f"Error loading page: {e}".encode('utf-8')
            )

        body = self.driver.page_source
        return HtmlResponse(
            url=self.driver.current_url,
            body=body,
            encoding='utf-8',
            request=request
        )

    def spider_closed(self, spider):
        logging.info("Closing Selenium WebDriver.")
        self.driver.quit()
