import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

class MotorsSpider(scrapy.Spider):
    name = 'motors'
    start_urls = ['https://www.motors.co.uk/car-72642888/?i=16&m=sr']

    def __init__(self, *args, **kwargs):
        super(MotorsSpider, self).__init__(*args, **kwargs)

        # Configure Chrome options to use Selenium with chrome driver
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Enable headless mode for no GUI
        chrome_options.add_argument("--disable-gpu")  # Necessary for headless on Windows

        # Specify the path where the chromedriver is located
        driver_path = '../chromedriver.exe'  # Make sure this is the correct path
        service = Service(driver_path)

        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def parse(self, response):
        # Selenium part to load the dynamically loaded page content
        url = response.url
        self.driver.get(url)

        self.driver.implicitly_wait(10)  # Give the page some time to load fully

        # Extract information with Selenium by inspecting the elements
        try:
            car_title = self.driver.find_element(By.XPATH, '//h1[@class="car-title"]').text
            year = self.driver.find_element(By.XPATH, '//span[@class="year"]').text
            litres = self.driver.find_element(By.XPATH, '//span[contains(text(),"litres")]').text  # Update based on what you find in DevTools
            hp = self.driver.find_element(By.XPATH, '//span[contains(text(),"hp")]').text
            miles = self.driver.find_element(By.XPATH, '//span[@class="miles"]').text
            fuel = self.driver.find_element(By.XPATH, '//span[@class="fuel"]').text
            transmission = self.driver.find_element(By.XPATH, '//span[@class="transmission"]').text
            body_style = self.driver.find_element(By.XPATH, '//span[@class="body-style"]').text
            price = self.driver.find_element(By.XPATH, '//span[@class="price"]').text

            # Print or return the results
            result = {
                'Car Title': car_title,
                'Year': year,
                'Litres': litres,
                'HP': hp,
                'Miles': miles,
                'Fuel Type': fuel,
                'Transmission': transmission,
                'Body Style': body_style,
                'Price': price
            }

            # Print the scraped data to the console or save it to a file/csv
            print(result)

        except Exception as e:
            print(f"Error while scraping the page: {e}")

        # Close Selenium driver after scraping the page
        self.driver.quit()
