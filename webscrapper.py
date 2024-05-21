import os
import selenium
from selenium import webdriver
import time
import io
import requests
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait

#Install Driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

try:
    # Navigate to the specified webpage
    driver.get("https://www.macrotrends.net/stocks/charts/GOOG/alphabet/eps-earnings-per-share-diluted")

    # Wait for the page to load
    time.sleep(5)  # You might want to use WebDriverWait for better practice

    # Print the title of the page to verify that it loaded
    print(f"Page title: {driver.title}")

    # If you want to perform additional actions, you can add them here
    # For example, if you want to take a screenshot of the webpage
    screenshot_path = 'screenshot.png'
    driver.save_screenshot(screenshot_path)
    print(f"Screenshot saved to {screenshot_path}")

    # Example of locating an element and interacting with it (if needed)
    # element = driver.find_element(By.ID, 'element_id')
    # element.click()

finally:
    # Close the browser
    driver.quit()