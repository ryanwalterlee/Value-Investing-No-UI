from text_format import add_colour, bold_red_text, bold_text
from tabulate import tabulate

def calc_projections(eps, pe, price):

    print(bold_text("Projections based on Past EPS and PE Ratios"))

    first_eps, last_eps = eps[0], eps[-1]
    if first_eps < 0 or last_eps < 0:
        print(bold_red_text("Cannot project future market price due to Negative EPS (DO NOT BUY)\n"))
        return
    if first_eps < last_eps:
        print(bold_red_text("Earnings is going down (DO NOT BUY)\n"))
        return
    if min(eps) < 0:
        print(bold_red_text("Negative EPS detected, earnings may not be consistent (DO NOT BUY)\n"))
        return
    
    avg_eps_growth = ((first_eps / last_eps) ** (1 / len(eps))) - 1

    avg_pe = sum(pe) / len(pe)

    ten_year_eps = round(((1 + avg_eps_growth) ** 10) * first_eps, 2)
    ten_year_market_price = round(ten_year_eps * avg_pe, 2)
    ten_year_max_market_price = round(ten_year_eps * max(pe), 2)
    ten_year_min_market_price = round(ten_year_eps * min(pe), 2)
    annual_growth_rate = (((ten_year_market_price / price) ** 0.1) - 1) * 100
    max_growth_rate = (((ten_year_max_market_price / price) ** 0.1) - 1) * 100
    min_growth_rate = (((ten_year_min_market_price / price) ** 0.1) - 1) * 100

    table_to_print = [
        ["Projections", "Values"],
        ["Current Price", price],
        ["EPS in 10 years", ten_year_eps],
        ["Market Price in 10 years", ten_year_market_price],
        ["Max Market Price", ten_year_max_market_price],
        ["Min Market Price", ten_year_min_market_price],
        ["Annual Growth Rate", add_colour(annual_growth_rate, 0.02, 0.05, 0)],
        ["Max Growth Rate", add_colour(max_growth_rate, 0.05, 0.08, 0)],
        ["Min Growth Rate", add_colour(min_growth_rate, 0.00, 0.02, 0)],
    ]

    print(tabulate(table_to_print, headers="firstrow", tablefmt="grid"))
    print()
