from webscrapper import scrape_eps_and_pe_ratio
from financial_data_api import get_financial_statement_data


def get_historical_data_header():
    header = ["Current year"]
    for i in range(1, 10):
        header.append("{} year ago".format(i))
    return header


def get_historical_data(ticker, log=None):
    eps_raw, pe_ratio_raw = scrape_eps_and_pe_ratio(ticker, log=log)
    financial_statement_data = get_financial_statement_data(ticker, log=log)
    return eps_raw, pe_ratio_raw, financial_statement_data
