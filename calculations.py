from webscrapper import scrape_eps_and_pe_ratio
from calculations_functions import calc_projections
from financial_data_api import get_financial_statement_data

ticker = input("Enter Ticker: ")

eps, pe_ratio = scrape_eps_and_pe_ratio(ticker)
financial_statement_data = get_financial_statement_data(ticker)

print(eps)
print(pe_ratio)
calc_projections(eps, pe_ratio, financial_statement_data.get_price())