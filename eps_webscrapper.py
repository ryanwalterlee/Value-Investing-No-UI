import os
import selenium
from selenium import webdriver
import time
import io
import requests
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

#Install Driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

def scrape_eps():
    
    # Navigate to the specified webpage
    driver.get("https://stockvalueinsights.com/AAPL/financials/")

    # wait until income statement eps row loads
    row = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div[comp-id='190']"))
    )

    # find all child elements in the parent div and put into an array
    child_divs = row.find_elements(By.CSS_SELECTOR, "div[role='gridcell']")

    # extract actual eps from child elements
    values = [grid_cell.text for grid_cell in child_divs]

    driver.quit()

    return values

print(scrape_eps())



        