from dotenv import load_dotenv
import os
import requests
import yfinance as yf
from financial_data_class import FinancialData

# Load environment variables from .env file
load_dotenv()

financial_modelling_prep_api_key = os.getenv("FINANCIAL_MODELLING_PREP_API_KEY")
financial_modelling_prep_url = "https://financialmodelingprep.com/stable"
income_statement_path = "income-statement"
balance_sheet_path = "balance-sheet-statement"
cash_flow_statement_path = "cash-flow-statement"
price_path = "quote"

def _log(log, message):
    if log:
        log(message)

def _get_field(df, *keys, default=0):
    for key in keys:
        if key in df.index:
            val = df.loc[key].iloc[0]
            if val is not None:
                return float(val)
    return default

def _get_from_yfinance(ticker, log=None):
    t = yf.Ticker(ticker)

    _log(log, "Fetching income statement...")
    income_stmt = t.income_stmt
    _log(log, "Received income statement")

    _log(log, "Fetching balance sheet...")
    balance_sheet = t.balance_sheet
    _log(log, "Received balance sheet")

    _log(log, "Fetching cash flow statement...")
    cashflow = t.cashflow
    _log(log, "Received cash flow statement")

    _log(log, "Fetching current price...")
    info = t.info
    price = info.get("currentPrice") or info.get("regularMarketPrice")
    _log(log, "Received current price")

    financial_statement_data = {
        "revenue":                        _get_field(income_stmt, "Total Revenue"),
        "grossProfit":                    _get_field(income_stmt, "Gross Profit"),
        "sellingAndMarketingExpenses":    _get_field(income_stmt, "Selling General And Administration"),
        "researchAndDevelopmentExpenses": _get_field(income_stmt, "Research And Development", default=0),
        "depreciationAndAmortization":    _get_field(income_stmt, "Reconciled Depreciation", "Depreciation And Amortization In Income Statement"),
        "operatingIncome":                _get_field(income_stmt, "Operating Income"),
        "interestExpense":                abs(_get_field(income_stmt, "Interest Expense", "Interest Expense Non Operating", default=0)),
        "netIncome":                      _get_field(income_stmt, "Net Income"),
        "longTermDebt":                   _get_field(balance_sheet, "Long Term Debt", "Long Term Debt And Capital Lease Obligation", default=0),
        "totalLiabilities":               _get_field(balance_sheet, "Total Liabilities Net Minority Interest"),
        "totalStockholdersEquity":        _get_field(balance_sheet, "Stockholders Equity", "Total Equity Gross Minority Interest"),
        "capitalExpenditure":             _get_field(cashflow, "Capital Expenditure"),
        "price":                          price,
    }

    return FinancialData(financial_statement_data)

def _get_from_fmp(ticker, log=None):
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
            raise _FMPSubscriptionError()
        if resp.status_code != 200:
            raise ValueError("API error for {} (HTTP {}): {}".format(name, resp.status_code, resp.text[:200]))
        data = resp.json()
        if not data:
            raise ValueError("Empty response for {} — ticker may not be supported".format(name))
        parsed[name] = data[0]

    relavant_keys = [
        "revenue", "grossProfit", "sellingAndMarketingExpenses",
        "researchAndDevelopmentExpenses", "depreciationAndAmortization",
        "operatingIncome", "interestExpense", "netIncome", "longTermDebt",
        "totalLiabilities", "totalStockholdersEquity", "capitalExpenditure", "price"
    ]
    combined = {**parsed["income statement"], **parsed["balance sheet"], **parsed["cash flow statement"], **parsed["current price"]}
    return FinancialData({key: combined[key] for key in relavant_keys})

class _FMPSubscriptionError(Exception):
    pass

def get_financial_statement_data(ticker, log=None):
    try:
        return _get_from_fmp(ticker, log)
    except _FMPSubscriptionError:
        _log(log, "{} not on FMP plan — falling back to Yahoo Finance...".format(ticker))
        return _get_from_yfinance(ticker, log)
