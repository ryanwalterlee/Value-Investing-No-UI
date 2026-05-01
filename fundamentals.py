from financial_data_class import FinancialData
from text_format import get_colour_class

def calc_fundamentals(data: FinancialData):
    """
    Returns a list of {"label", "value", "color"} dicts for each financial ratio.
    """
    gross_profit_margin = data.get_gross_profit() / data.get_revenue()
    percentage_sga = data.get_selling_and_marketing_expenses() / data.get_gross_profit()
    percentage_rd = data.get_research_and_development_expenses() / data.get_gross_profit()
    percentage_depreciation = data.get_depreciation_and_amortization() / data.get_gross_profit()
    interest_expense_over_operating_income = data.get_interest_expense() / data.get_operating_income()
    profit_margin = data.get_net_income() / data.get_revenue()
    long_term_debt_to_net_earning_ratio = data.get_long_term_debt() / data.get_net_income()
    return_on_equity = data.get_net_income() / data.get_total_stockholders_equity()
    percentage_capital_expenditure = -data.get_capital_expenditure() / data.get_net_income()

    return [
        {"label": "Gross Profit Margin",                    "value": round(gross_profit_margin, 2),                    "color": get_colour_class(gross_profit_margin, 0.3, 0.4, 0)},
        {"label": "Percentage SGA",                         "value": round(percentage_sga, 2),                         "color": get_colour_class(percentage_sga, 0.3, 0.6, 1)},
        {"label": "Percentage RND",                         "value": round(percentage_rd, 2),                          "color": get_colour_class(percentage_rd, 0.3, 0.5, 1)},
        {"label": "Percentage Depreciation",                "value": round(percentage_depreciation, 2),                "color": get_colour_class(percentage_depreciation, 0.1, 0.2, 1)},
        {"label": "Interest Expense Over Operating Income", "value": round(interest_expense_over_operating_income, 2), "color": get_colour_class(interest_expense_over_operating_income, 0.1, 0.3, 1)},
        {"label": "Profit Margin",                          "value": round(profit_margin, 2),                          "color": get_colour_class(profit_margin, 0.1, 0.2, 0)},
        {"label": "Long Term Debt to Net Earning Ratio",    "value": round(long_term_debt_to_net_earning_ratio, 2),    "color": get_colour_class(long_term_debt_to_net_earning_ratio, 4, 8, 1)},
        {"label": "Return on Equity",                       "value": round(return_on_equity, 2),                       "color": get_colour_class(return_on_equity, 0.1, 0.2, 0)},
        {"label": "Percentage Capital Expenditure",         "value": round(percentage_capital_expenditure, 2),         "color": get_colour_class(percentage_capital_expenditure, 0.3, 0.5, 1)},
    ]
