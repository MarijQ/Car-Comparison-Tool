from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException

# Initialize WebDriver
driver = webdriver.Chrome()

# URL to scrape content
content_url = "https://www.carwow.co.uk/used-cars"

# Base URL for pagination (with placeholder for the page number)
base_url = "https://www.carwow.co.uk/used-cars?age=0%2C9&budget=0%2C150000&mileage=0%2C100000&stock_type=used&pagination%5Bcurrent_page%5D={page}&pagination%5Bper_page%5D=12"

# List to track already scraped car links
scraped_links = []

# Gradual scrolling parameters
scroll_pause_time = 4  # Time to wait between scrolls
scroll_step = 500  # Scroll step size in pixels

def scrape_page_content(driver):
    """
    Scrapes content from a single page of cars.
    """
    try:
        # Scroll gradually and process visible cars
        total_height = driver.execute_script("return document.body.scrollHeight")
        current_scroll_position = 0

        while current_scroll_position < total_height:
            cars = driver.find_elements(By.CSS_SELECTOR, 'article.card-generic')

            for car_index in range(len(cars)):
                try:
                    # Re-fetch the car elements to avoid stale references
                    cars = driver.find_elements(By.CSS_SELECTOR, 'article.card-generic')
                    car = cars[car_index]

                    # Extract the link for the car's individual page
                    link = car.find_element(By.CSS_SELECTOR, 'div.card-generic__section div.card-generic__ctas a').get_attribute('href')

                    if link not in scraped_links:
                        scraped_links.append(link)

                        # Print the car link for debugging
                        print({'link': link})

                        # Open the car's individual page
                        driver.get(link)
                        time.sleep(2)  # Wait for the page to load

                        # Extract car details
                        try:
                            car_name = driver.find_element(By.CSS_SELECTOR, 'span.deal-title__model').text
                        except NoSuchElementException:
                            car_name = "N/A"

                        try:
                            price = driver.find_element(By.CSS_SELECTOR, 'div.deal-pricing__carwow-price').text
                        except NoSuchElementException:
                            price = "N/A"

                        print({'car_name': car_name, 'price': price})

                        details = driver.find_elements(By.CSS_SELECTOR, 'div.summary-list__item')
                        for div in details:
                            try:
                                title = div.find_element(By.CSS_SELECTOR, 'dt').text
                                detail = div.find_element(By.CSS_SELECTOR, 'dd').text
                                print(f'{title}: {detail}')
                            except NoSuchElementException:
                                continue

                        # Return to the main page
                        driver.back()
                        time.sleep(2)

                except (NoSuchElementException, StaleElementReferenceException) as e:
                    print(f"Error processing car: {e}")

            # Scroll down gradually
            current_scroll_position += scroll_step
            driver.execute_script(f"window.scrollTo(0, {current_scroll_position});")
            time.sleep(scroll_pause_time)

            # Update total height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if current_scroll_position >= new_height:
                print("No more new cars to scrape on this page. Exiting...")
                break

    except Exception as e:
        print(f"Error during page scraping: {e}")

def get_page_links():
    """
    Fetches all pagination links and returns them as a list.
    """
    total_pages = 100  # Manually set the total number of pages (could be dynamically scraped as well)
    all_page_links = [base_url.format(page=page) for page in range(1, total_pages + 1)]
    return all_page_links

# Main scraping process
try:
    # Get the pagination links
    page_links = get_page_links()
    print(f"Pagination Links: {page_links}")

    # Loop through each page link
    for page_link in page_links:
        try:
            driver.get(page_link)  # Navigate to the page
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'article.card-generic'))
            )
            time.sleep(2)  # Allow the page to load

            # Scrape data from the current page
            scrape_page_content(driver)

        except (TimeoutException, Exception) as e:
            print(f"Error processing page {page_link}: {e}")

finally:
    # Close the browser
    driver.quit()