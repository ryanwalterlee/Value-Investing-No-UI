class FinancialData:

    def __init__(self, financial_data):
        self.financial_data = financial_data

    def __str__(self):
        return str(self.financial_data)

    def get_revenue(self):
        return self.financial_data.get("revenue")

    def get_gross_profit(self):
        return self.financial_data.get("grossProfit")

    def get_selling_and_marketing_expenses(self):
        return self.financial_data.get("sellingAndMarketingExpenses")

    def get_research_and_development_expenses(self):
        return self.financial_data.get("researchAndDevelopmentExpenses")

    def get_depreciation_and_amortization(self):
        return self.financial_data.get("depreciationAndAmortization")

    def get_operating_income(self):
        return self.financial_data.get("operatingIncome")

    def get_interest_expense(self):
        return self.financial_data.get("interestExpense")

    def get_net_income(self):
        return self.financial_data.get("netIncome")

    def get_long_term_debt(self):
        return self.financial_data.get("longTermDebt")

    def get_total_liabilities(self):
        return self.financial_data.get("totalLiabilities")

    def get_total_stockholders_equity(self):
        return self.financial_data.get("totalStockholdersEquity")

    def get_capital_expenditure(self):
        return self.financial_data.get("capitalExpenditure")

    def get_price(self):
        return self.financial_data.get("price")