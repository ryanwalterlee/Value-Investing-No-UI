from projections import calc_projections
from fundamentals import calc_fundamentals
from historical import get_historical_data
from text_format import bold_text

print()
ticker = input(bold_text("Enter Ticker: "))
print()

eps, pe_ratio, financial_statement_data = get_historical_data(ticker)
calc_projections(eps, pe_ratio, financial_statement_data.get_price())
calc_fundamentals(financial_statement_data)