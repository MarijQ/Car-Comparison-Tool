import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Configure WebDriver options
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Initialize WebDriver
driver = webdriver.Chrome(options=options)

# URLs
base_url = "https://www.carwow.co.uk/used-cars?age=0%2C9&budget=0%2C150000&mileage=0%2C100000&stock_type=used&pagination%5Bcurrent_page%5D={page}&pagination%5Bper_page%5D=12"
json_file_path = 'car_data.json'

# Scraped data tracking
scraped_links = set()  # Use a set to prevent duplicate links
all_car_data = []  # Store car data

# Scroll and retry parameters
scroll_pause_time = 3
scroll_step = 500
total_pages = 100  # Total pages to scrape


def append_to_json_file(data, file_path):
    """Append car data to a JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = []  # Start fresh if file is missing or empty

    existing_data.append(data)

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)


def scrape_car_details(driver, link):
    """Scrape details from an individual car page."""
    driver.get(link)
    time.sleep(3)  # Allow the page to load

    car_data = {
        "link": link,
        "dealer_name": "N/A",
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
    }

    try:
        car_data["dealer_name"] = driver.find_element(By.CSS_SELECTOR, 'div.dealership-info__title').text
    except:
        pass

    try:
        car_data["car_name"] = driver.find_element(By.CSS_SELECTOR, 'span.deal-title__model').text
    except:
        pass

    try:
        car_data["price"] = driver.find_element(By.CSS_SELECTOR, 'div.deal-pricing__carwow-price').text
    except:
        pass

    details = driver.find_elements(By.CSS_SELECTOR, 'div.summary-list__item')
    for detail in details:
        try:
            title = detail.find_element(By.CSS_SELECTOR, 'dt').text.strip().lower()
            value = detail.find_element(By.CSS_SELECTOR, 'dd').text.strip()
            if title == "year":
                car_data["year"] = value
            elif title == "mileage":
                car_data["mileage"] = value
            elif title == "engine size":
                car_data["engine_size"] = value
            elif title == "engine power":
                car_data["engine_power"] = value
            elif title == "transmission":
                car_data["transmission"] = value
            elif title == "fuel":
                car_data["fuel"] = value
            elif title == "doors":
                car_data["doors"] = value
            elif title == "seats":
                car_data["seats"] = value
            elif title == "colour":
                car_data["colour"] = value
            elif title == "registration number":
                car_data["registration_number"] = value
            elif title == "previous owners":
                car_data["previous_owners"] = value
            elif title == "co2 emissions":
                car_data["co2_emissions"] = value
            elif title == "emissions standard":
                car_data["emissions_standard"] = value
            elif title == "insurance group":
                car_data["insurance_group"] = value
            elif title == "acceleration (0-62mph)":
                car_data["acceleration_0_62mph"] = value
            elif title == "top speed":
                car_data["top_speed"] = value
            elif title == "average mpg":
                car_data["average_mpg"] = value
        except:
            continue

    return car_data


def scrape_page_content(driver):
    """Scrape all cars from a single page."""
    cars = driver.find_elements(By.CSS_SELECTOR, 'article.card-generic')
    for car in cars:
        try:
            link = car.find_element(By.CSS_SELECTOR, 'div.card-generic__ctas a').get_attribute('href')
            if link in scraped_links:
                continue

            scraped_links.add(link)
            car_data = scrape_car_details(driver, link)
            append_to_json_file(car_data, json_file_path)
        except Exception as e:
            print(f"Error processing car: {e}")


def get_page_links():
    """Generate all pagination links."""
    return [base_url.format(page=page) for page in range(1, total_pages + 1)]


# Main scraping process
try:
    page_links = get_page_links()
    for page_link in page_links:
        try:
            driver.get(page_link)
            time.sleep(3)
            scrape_page_content(driver)
        except Exception as e:
            print(f"Error processing page {page_link}: {e}")
finally:
    driver.quit()