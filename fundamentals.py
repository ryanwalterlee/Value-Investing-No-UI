from financial_data_class import FinancialData
from text_format import add_colour, bold_text
from tabulate import tabulate

def calc_fundamentals(data: FinancialData):

    # print(data)

    gross_profit_margin = data.get_gross_profit() / data.get_revenue()
    percentage_sga = data.get_selling_and_marketing_expenses() / data.get_gross_profit()
    percentage_rd = data.get_research_and_development_expenses() / data.get_gross_profit()
    percentage_depreciation = data.get_depreciation_and_amortization() / data.get_gross_profit()
    interest_expense_over_operating_income = data.get_interest_expense() / data.get_operating_income()
    profit_margin = data.get_net_income() / data.get_revenue()
    long_term_debt_to_net_earning_ratio = data.get_long_term_debt() / data.get_net_income()
    return_on_equity = data.get_net_income() / data.get_total_stockholders_equity()
    percentage_capital_expenditure = - data.get_capital_expenditure() / data.get_net_income()

    table_to_print = [
        ["Ratio", "Value"],
        ["Gross Profit Margin", add_colour(gross_profit_margin, 0.3, 0.4, 0)],
        ["Percentage SGA", add_colour(percentage_sga, 0.3, 0.6, 1)],
        ["Percentage RND", add_colour(percentage_rd, 0.3, 0.5, 1)],
        ["Percentage Depreciation", add_colour(percentage_depreciation, 0.1, 0.2, 1)],
        ["Interest Expense Over Operating Income", add_colour(interest_expense_over_operating_income, 0.1, 0.3, 1)],
        ["Profit Margin", add_colour(profit_margin, 0.1, 0.2, 0)],
        ["Long Term Debt to Net Earning Ratio", add_colour(long_term_debt_to_net_earning_ratio, 4, 8, 1)],
        ["Return on Equity", add_colour(return_on_equity, 0.1, 0.2, 0)],
        ["Percentage Capital Expenditure", add_colour(percentage_capital_expenditure, 0.3, 0.5, 1)],
    ]

    print(bold_text("Financial Soundness of Company based on Financial Ratios"))
    print(tabulate(table_to_print, headers="firstrow", tablefmt="grid"))
    print()

    # print(table_to_print)
    return table_to_print
