from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Initialize WebDriver
driver = webdriver.Chrome()

# Base URL with a placeholder for page number
base_url = "https://www.carwow.co.uk/used-cars?age=0%2C9&budget=0%2C150000&mileage=0%2C100000&stock_type=used&pagination%5Bcurrent_page%5D={page}&pagination%5Bper_page%5D=12"

# Total number of pages (manually determined or scraped from the pagination structure)
total_pages = 100

try:
    # Generate all page URLs
    all_page_links = [base_url.format(page=page) for page in range(1, total_pages + 1)]

    # Print the generated URLs for debugging
    for page_url in all_page_links:
        print(f"Page URL: {page_url}")

finally:
    # Close the browser
    driver.quit()