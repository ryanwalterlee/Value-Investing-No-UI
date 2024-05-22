from tabulate import tabulate
from webscrapper import scrape_eps_and_pe_ratio
from financial_data_api import get_financial_statement_data
from text_format import bold_text

def get_historical_data_header():
    header = ["Current year"]
    for i in range(1, 10):
        header.append("{} year ago".format(i))
    return header

def get_historical_data(ticker):

    eps_raw, pe_ratio_raw = scrape_eps_and_pe_ratio(ticker)
    financial_statement_data = get_financial_statement_data(ticker)

    header = get_historical_data_header()

    eps = [header, eps_raw]
    pe_ratio = [header, pe_ratio_raw]

    print(bold_text("Past 10 years EPS"))
    print(tabulate(eps, headers="firstrow", tablefmt="grid"))
    print()
    print(bold_text("Past 10 years PE ratio"))
    print(tabulate(pe_ratio, headers="firstrow", tablefmt="grid"))
    print()

    return eps_raw, pe_ratio_raw, financial_statement_data