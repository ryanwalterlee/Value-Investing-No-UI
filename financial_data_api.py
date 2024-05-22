from dotenv import load_dotenv
import os
import requests
from financial_data_class import FinancialData

# Load environment variables from .env file
load_dotenv()

financial_modelling_prep_api_key = os.getenv("FINANCIAL_MODELLING_PREP_API_KEY")
financial_modelling_prep_url = "https://financialmodelingprep.com/api/v3"
income_statement_path = "income-statement"
balance_sheet_path = "balance-sheet-statement"
cash_flow_statement_path = "cash-flow-statement"
price_path = "quote"
params = {
        "apikey": financial_modelling_prep_api_key,
        "limit": 1
    }

relavant_keys = [
    "revenue",
    "grossProfit",
    "sellingAndMarketingExpenses",
    "researchAndDevelopmentExpenses",
    "depreciationAndAmortization",
    "operatingIncome",
    "interestExpense",
    "netIncome",
    "longTermDebt",
    "totalLiabilities",
    "totalStockholdersEquity",
    "capitalExpenditure",
    "price"
]

def get_financial_statement_data(ticker):
    """
    Sends 3 GET requests to financial modelling prep to get the 3 financial statements. Also filters for the relavant keys only.

    Arguments:
        ticker (string): stock ticker

    Returns:
        dict: A dictionary containing the following keys:
            - revenue
            - grossProfit
            - sellingAndMarketingExpenses
            - researchAndDevelopmentExpenses
            - depreciationAndAmortization
            - operatingIncome
            - interestExpense
            - netIncome
            - longTermDebt
            - totalLiabilities
            - totalStockholdersEquity
            - capitalExpenditure
    """

    income_statement_response = requests.get("{}/{}/{}".format(financial_modelling_prep_url, income_statement_path, ticker), params=params)
    balance_sheet_response = requests.get("{}/{}/{}".format(financial_modelling_prep_url, balance_sheet_path, ticker), params=params)
    cash_flow_statement_response = requests.get("{}/{}/{}".format(financial_modelling_prep_url, cash_flow_statement_path, ticker), params=params)
    price_response = requests.get("{}/{}/{}".format(financial_modelling_prep_url, price_path, ticker), params=params)
    
    combined_response_data = {
        **income_statement_response.json()[0], 
        **balance_sheet_response.json()[0], 
        **cash_flow_statement_response.json()[0],
        **price_response.json()[0],
    }

    financial_statement_data = {key: combined_response_data[key] for key in relavant_keys}

    return FinancialData(financial_statement_data)
    