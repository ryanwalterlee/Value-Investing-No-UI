from text_colour_mapping import RED, YELLOW, GREEN

def find_colour(value, green_value, red_value):
    if value > green_value:
        return GREEN
    elif value < red_value:
        return RED
    else:
        return YELLOW

def calc_projections(eps, pe, price):

    first_eps, last_eps = eps[0], eps[-1]
    avg_eps_growth = ((first_eps / last_eps) ** 0.1) - 1

    avg_pe = sum(pe) / len(pe)

    ten_year_eps = ((1 + avg_eps_growth) ** 10) * first_eps
    ten_year_market_price = ten_year_eps * avg_pe
    ten_year_max_market_price = ten_year_eps * max(pe)
    ten_year_min_market_price = ten_year_eps * min(pe)
    annual_growth_rate = round((((ten_year_market_price / price) ** 0.1) - 1) * 100, 2)
    max_growth_rate = round((((ten_year_max_market_price / price) ** 0.1) - 1) * 100, 2)
    min_growth_rate = round((((ten_year_min_market_price / price) ** 0.1) - 1) * 100, 2)

    print("Current Price: ${}".format(price))
    print("EPS in 10 years: ${}".format(ten_year_eps))
    print("Market Price in 10 years: ${}".format(ten_year_market_price))
    print("Max Market Price: ${}".format(ten_year_max_market_price))
    print("Min Market Price: ${}".format(ten_year_min_market_price))
    print("{}Annual Growth Rate: {}%".format(find_colour(annual_growth_rate, 0.05, 0.02), annual_growth_rate))
    print("{}Max Growth Rate: {}%".format(find_colour(max_growth_rate, 0.08, 0.05), max_growth_rate))
    print("{}Min Growth Rate: {}%".format(find_colour(min_growth_rate, 0.02, 0.00), min_growth_rate))


