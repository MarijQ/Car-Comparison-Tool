from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Initialize the WebDriver
driver = webdriver.Chrome()

# Navigate to the URL
base_url = "https://quotes.carwow.co.uk/deals/c8d64fa3cdc06527e2b6ca96a978ee61"
driver.get(base_url)

# Allow the page to load
time.sleep(5)  # Adjust sleep time as necessary, or use WebDriver waits

# Locate the element and extract the dealer name
dealer_name = driver.find_element(By.CSS_SELECTOR, 'div.dealership-info div.dealership-info__main div.dealership-info__inner div.dealership-info__title').text

# Print the dealer name
print(dealer_name)

# Close the driver
driver.quit()