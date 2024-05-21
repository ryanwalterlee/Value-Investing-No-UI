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

def scrape_eps(ticker):
    
    # Navigate to the specified webpage
    driver.get("https://companiesmarketcap.com")

    # wait until income statement eps row loads
    search_bar = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[id='search-input']"))
    )

    # enter ticker in search bar
    search_bar.send_keys(ticker)
    
    dropdown_menu = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div[id='typeahead-search-results']"))
    )

    # wait for dropdown menu to drop
    time.sleep(3)

    # select first option in dropdown
    ticker_to_click = dropdown_menu.find_elements(By.XPATH, ".//*")[0]
    href = ticker_to_click.get_attribute('href')
    href = href.replace('/marketcap/', '/eps/')
    
    # jump straight to the page to avoid ads
    driver.get(href)
    
    # Locate the table
    table = driver.find_element(By.CSS_SELECTOR, "table.table")

    # Locate the rows in the table body
    rows = table.find_elements(By.XPATH, "./tbody/tr")

    # Extract the second <td> from each row, which contains the dollar amounts
    historical_eps = []
    for row in rows:
        td_element = row.find_elements(By.TAG_NAME, "td")[1]  # index 1 for the second <td>
        historical_eps.append(td_element.text)

    driver.quit()

    return historical_eps

print(scrape_eps('aapl'))



        