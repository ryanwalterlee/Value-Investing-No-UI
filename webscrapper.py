from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


def scrape_second_column(driver):
    table = driver.find_element(By.CSS_SELECTOR, "table.table")
    rows = table.find_elements(By.XPATH, "./tbody/tr")
    results = []
    for row in rows:
        td_element = row.find_elements(By.TAG_NAME, "td")[1]
        results.append(td_element.text)
    return results


def convert_to_float(values):
    result = []
    for value in values:
        cleaned_value = value.replace('$', '')
        result.append(float(cleaned_value))
    return result


def scrape_eps_and_pe_ratio(ticker, log=None):
    def _log(message):
        if log:
            log(message)

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        _log("Opening companiesmarketcap.com...")
        driver.get("https://companiesmarketcap.com")

        search_bar = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[id='search-input']"))
        )

        _log("Searching for {}...".format(ticker))
        search_bar.send_keys(ticker)

        dropdown_menu = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[id='typeahead-search-results']"))
        )

        time.sleep(3)

        ticker_to_click = dropdown_menu.find_elements(By.XPATH, ".//*")[0]
        href = ticker_to_click.get_attribute('href')
        href = href.replace('/marketcap/', '/eps/')

        _log("Fetching historical EPS...")
        driver.get(href)
        historical_eps = scrape_second_column(driver)
        _log("Received historical EPS")

        href = href.replace('/eps/', '/pe-ratio/')

        _log("Fetching historical PE ratio...")
        driver.get(href)
        historical_pe_ratio = scrape_second_column(driver)
        _log("Received historical PE ratio")
    finally:
        driver.quit()

    return convert_to_float(historical_eps[:10]), convert_to_float(historical_pe_ratio[:10])
