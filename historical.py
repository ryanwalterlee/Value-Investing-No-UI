from webscrapper import scrape_eps_and_pe_ratio
from financial_data_api import get_financial_statement_data
from financial_data_class import FinancialData
import cache


def get_historical_data_header(length=10):
    header = ["Current year"]
    for i in range(1, length):
        header.append("{} year ago".format(i))
    return header


def get_historical_data(ticker, log=None):
    def _log(msg):
        if log:
            log(msg)

    cached = cache.get(ticker)
    if cached:
        _log("Loaded {} from cache".format(ticker))
        eps, pe_ratio, financial_data_dict = cached
        return eps, pe_ratio, FinancialData(financial_data_dict)

    eps, pe_ratio = scrape_eps_and_pe_ratio(ticker, log=log)
    financial_data = get_financial_statement_data(ticker, log=log)

    cache.set(ticker, eps, pe_ratio, financial_data.financial_data)

    return eps, pe_ratio, financial_data
