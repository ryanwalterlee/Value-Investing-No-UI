import pytest
from unittest.mock import patch, Mock
from financial_data_api import get_financial_statement_data
from financial_data_class import FinancialData

@patch('requests.get')
def test_get_financial_statement_data(mock_get):
    # Create mock responses for each endpoint
    mock_income_statement_response = Mock()
    mock_income_statement_response.json.return_value = [{
        "revenue": 1000000,
        "grossProfit": 500000,
        "sellingAndMarketingExpenses": 100000,
        "researchAndDevelopmentExpenses": 80000,
        "depreciationAndAmortization": 60000,
        "operatingIncome": 300000,
        "interestExpense": 20000,
        "netIncome": 280000
    }]

    mock_balance_sheet_response = Mock()
    mock_balance_sheet_response.json.return_value = [{
        "longTermDebt": 200000,
        "totalLiabilities": 500000,
        "totalStockholdersEquity": 300000
    }]

    mock_cash_flow_statement_response = Mock()
    mock_cash_flow_statement_response.json.return_value = [{
        "capitalExpenditure": 70000
    }]

    mock_price_response = Mock()
    mock_price_response.json.return_value = [{
        "price": 150
    }]

    # Set the return_value of the mock_get method to each of the mock responses
    mock_get.side_effect = [mock_income_statement_response, mock_balance_sheet_response, mock_cash_flow_statement_response, mock_price_response]

    # Call the function to test
    ticker = "AAPL"
    financial_data = get_financial_statement_data(ticker)

    # Define expected data
    expected_data = {
        "revenue": 1000000,
        "grossProfit": 500000,
        "sellingAndMarketingExpenses": 100000,
        "researchAndDevelopmentExpenses": 80000,
        "depreciationAndAmortization": 60000,
        "operatingIncome": 300000,
        "interestExpense": 20000,
        "netIncome": 280000,
        "longTermDebt": 200000,
        "totalLiabilities": 500000,
        "totalStockholdersEquity": 300000,
        "capitalExpenditure": 70000,
        "price": 150
    }

    # Check if FinancialData object contains the expected data
    assert isinstance(financial_data, FinancialData)
    assert financial_data.financial_data == expected_data
