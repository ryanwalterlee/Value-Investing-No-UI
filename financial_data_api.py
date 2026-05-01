from dotenv import load_dotenv
import os
import requests
from financial_data_class import FinancialData

# Load environment variables from .env file
load_dotenv()

financial_modelling_prep_api_key = os.getenv("FINANCIAL_MODELLING_PREP_API_KEY")
financial_modelling_prep_url = "https://financialmodelingprep.com/stable"
income_statement_path = "income-statement"
balance_sheet_path = "balance-sheet-statement"
cash_flow_statement_path = "cash-flow-statement"
price_path = "quote"

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

def _log(log, message):
    if log:
        log(message)

def get_financial_statement_data(ticker, log=None):
    params = {
        "symbol": ticker,
        "apikey": financial_modelling_prep_api_key,
        "limit": 1
    }

    _log(log, "Fetching income statement...")
    income_statement_response = requests.get("{}/{}".format(financial_modelling_prep_url, income_statement_path), params=params)
    _log(log, "Received income statement")

    _log(log, "Fetching balance sheet...")
    balance_sheet_response = requests.get("{}/{}".format(financial_modelling_prep_url, balance_sheet_path), params=params)
    _log(log, "Received balance sheet")

    _log(log, "Fetching cash flow statement...")
    cash_flow_statement_response = requests.get("{}/{}".format(financial_modelling_prep_url, cash_flow_statement_path), params=params)
    _log(log, "Received cash flow statement")

    _log(log, "Fetching current price...")
    price_response = requests.get("{}/{}".format(financial_modelling_prep_url, price_path), params=params)
    _log(log, "Received current price")

    responses = {
        "income statement":    income_statement_response,
        "balance sheet":       balance_sheet_response,
        "cash flow statement": cash_flow_statement_response,
        "current price":       price_response,
    }
    parsed = {}
    for name, resp in responses.items():
        if resp.status_code == 402:
            raise ValueError("{} is not available on your FMP subscription plan.".format(ticker))
        if resp.status_code != 200:
            raise ValueError("API error for {} (HTTP {}): {}".format(name, resp.status_code, resp.text[:200]))
        data = resp.json()
        if not data:
            raise ValueError("Empty response for {} — ticker may not be supported".format(name))
        parsed[name] = data[0]

    combined_response_data = {**parsed["income statement"], **parsed["balance sheet"], **parsed["cash flow statement"], **parsed["current price"]}

    financial_statement_data = {key: combined_response_data[key] for key in relavant_keys}

    return FinancialData(financial_statement_data)
