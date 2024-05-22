from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Configure Chrome options for headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")

# Install Driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

def scrape_second_column():
    """
    Scrape 2nd column of table on companiesmarketcap

    Returns:
        list(string): list of the data in the second column
    """

    # Locate the table
    table = driver.find_element(By.CSS_SELECTOR, "table.table")

    # Locate the rows in the table body
    rows = table.find_elements(By.XPATH, "./tbody/tr")

    # Extract the second <td> from each row, which contains the dollar amounts
    results = []
    for row in rows:
        td_element = row.find_elements(By.TAG_NAME, "td")[1]  # get 2nd column
        results.append(td_element.text)

    return results

def convert_to_float(values):
    result = []
    for value in values:
        # Remove any non-numeric characters
        cleaned_value = value.replace('$', '')
        # Convert to integer
        result.append(float(cleaned_value))
    return result


def scrape_eps_and_pe_ratio(ticker):
    """
    Goes to companiesmarketcap.com to scrape eps and pe ratio

    Args:
        ticker (string): Ticker of stock
    
    Returns:
        list(string), list(string): eps list and pe ratio list
    """
    
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
    
    historical_eps = scrape_second_column()

    href = href.replace('/eps/', '/pe-ratio/')

    # jump straight to the page to avoid ads
    driver.get(href)

    historical_pe_ratio = scrape_second_column()

    driver.quit()

    return convert_to_float(historical_eps[:10]), convert_to_float(historical_pe_ratio[:10])




        