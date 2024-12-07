import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

# Initialize WebDriver
driver = webdriver.Chrome()

# URL to scrape content
content_url = "https://www.carwow.co.uk/used-cars"

# Base URL for pagination (with placeholder for the page number)
base_url = "https://www.carwow.co.uk/used-cars?age=0%2C9&budget=0%2C150000&mileage=0%2C100000&stock_type=used&pagination%5Bcurrent_page%5D={page}&pagination%5Bper_page%5D=12"

# List to track already scraped car links and store all the car data
scraped_links = []
all_car_data = []  # List to store car data dictionaries

# Gradual scrolling parameters
scroll_pause_time = 4  # Time to wait between scrolls
scroll_step = 500  # Scroll step size in pixels

# Open JSON file for writing
with open('car_data.json', 'w', encoding='utf-8') as json_file:

    def scrape_page_content(driver):
        """
        Scrapes content from a single page of cars and appends the data to a list.
        """
        total_height = driver.execute_script("return document.body.scrollHeight")
        current_scroll_position = 0
        last_scroll_position = 0  # Tracks the last scroll position

        while True:
            # Fetch the car elements currently visible
            cars = driver.find_elements(By.CSS_SELECTOR, 'article.card-generic')

            # Loop through each car element
            for car_index in range(len(cars)):
                try:
                    # Re-fetch the car elements to avoid stale references
                    cars = driver.find_elements(By.CSS_SELECTOR, 'article.card-generic')

                    # Extract the link for the car's individual page
                    link = cars[car_index].find_element(By.CSS_SELECTOR, 'div.card-generic__section div.card-generic__ctas a').get_attribute('href')

                    # Skip if the link has already been scraped
                    if link in scraped_links:
                        continue  # Skip to the next car

                    # Open the car's individual page
                    driver.get(link)
                    time.sleep(3)  # Give it some time to load the page

                    # Extract the car's detailed information (e.g., name, price, and specifications)
                    car_data = {
                        "link": link,
                        "car_name": "N/A",
                        "price": "N/A",
                        "year": "N/A",
                        "mileage": "N/A",
                        "engine_size": "N/A",
                        "engine_power": "N/A",
                        "transmission": "N/A",
                        "fuel": "N/A",
                        "doors": "N/A",
                        "seats": "N/A",
                        "colour": "N/A",
                        "registration_number": "N/A",
                        "previous_owners": "N/A",
                        "co2_emissions": "N/A",
                        "emissions_standard": "N/A",
                        "insurance_group": "N/A",
                        "acceleration_0_62mph": "N/A",
                        "top_speed": "N/A",
                        "average_mpg": "N/A",
                        "boot_seats_up": "N/A",
                        "boot_seats_down": "N/A",
                        "safety_rating": "N/A"
                    }

                    # Extract car name and price
                    try:
                        car_data["car_name"] = driver.find_element(By.CSS_SELECTOR, 'span.deal-title__model').text
                    except:
                        pass

                    try:
                        car_data["price"] = driver.find_element(By.CSS_SELECTOR, 'div.deal-pricing__carwow-price').text
                    except:
                        pass

                    # Extract other details from the summary list
                    details = driver.find_elements(By.CSS_SELECTOR, 'div.summary-list__item')
                    for div in details:
                        try:
                            title = div.find_element(By.CSS_SELECTOR, 'dt').text
                            detail = div.find_element(By.CSS_SELECTOR, 'dd').text
                            if title.lower() == "year":
                                car_data["year"] = detail
                            elif title.lower() == "mileage":
                                car_data["mileage"] = detail
                            elif title.lower() == "engine size":
                                car_data["engine_size"] = detail
                            elif title.lower() == "engine power":
                                car_data["engine_power"] = detail
                            elif title.lower() == "transmission":
                                car_data["transmission"] = detail
                            elif title.lower() == "fuel":
                                car_data["fuel"] = detail
                            elif title.lower() == "doors":
                                car_data["doors"] = detail
                            elif title.lower() == "seats":
                                car_data["seats"] = detail
                            elif title.lower() == "colour":
                                car_data["colour"] = detail
                            elif title.lower() == "registration number":
                                car_data["registration_number"] = detail
                            elif title.lower() == "previous owners":
                                car_data["previous_owners"] = detail
                            elif title.lower() == "co2 emissions":
                                car_data["co2_emissions"] = detail
                            elif title.lower() == "emissions standard":
                                car_data["emissions_standard"] = detail
                            elif title.lower() == "insurance group":
                                car_data["insurance_group"] = detail
                            elif title.lower() == "acceleration (0-62mph)":
                                car_data["acceleration_0_62mph"] = detail
                            elif title.lower() == "top speed":
                                car_data["top_speed"] = detail
                            elif title.lower() == "average mpg":
                                car_data["average_mpg"] = detail
                            elif title.lower() == "boot seats up":
                                car_data["boot_seats_up"] = detail
                            elif title.lower() == "boot seats down":
                                car_data["boot_seats_down"] = detail
                            elif title.lower() == "safety rating":
                                car_data["safety_rating"] = detail
                        except Exception as e:
                            print(f"Error fetching detail: {e}")

                    # Add the car data to the list
                    all_car_data.append(car_data)

                    # Add the link to the list of scraped links
                    scraped_links.append(link)

                    # Return to the main page after scraping the car details
                    driver.back()
                    time.sleep(3)  # Wait for the main page to load again

                except Exception as e:
                    print(f"Error processing car: {e}")

            # Gradual scrolling after processing all visible cars
            current_scroll_position += scroll_step
            driver.execute_script(f"window.scrollTo(0, {current_scroll_position});")
            time.sleep(scroll_pause_time)

            # Check if new content has loaded
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_scroll_position:  # If no new content is loaded, stop
                print("No more new cars to scrape on this page. Exiting...")
                break

            last_scroll_position = new_height

    def get_page_links():
        """
        Fetches all pagination links and returns them as a list.
        """
        total_pages = 100  # Manually set the total number of pages (could be dynamically scraped as well)
        all_page_links = [base_url.format(page=page) for page in range(1, total_pages + 1)]
        return all_page_links


    # Main scraping process
    try:
        # First, get the pagination links
        page_links = get_page_links()
        print(f"Pagination Links: {page_links}")

        # Loop through each page link
        for page_link in page_links:
            try:
                driver.get(page_link)  # Navigate to the page
                time.sleep(3)  # Allow the page to load

                # Scrape data from the current page
                scrape_page_content(driver)

            except Exception as e:
                print(f"Error processing page {page_link}: {e}")

        # After scraping all the pages, write all the car data at once
        json.dump(all_car_data, json_file, ensure_ascii=False, indent=4)

    finally:
        # Close the browser
        driver.quit()