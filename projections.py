from text_format import get_colour_class

def calc_projections(eps, pe, price):
    """
    Returns projection data as a dict.
    On invalid input returns {"error": message}.
    On success returns {"rows": [{"label", "value", "color"}, ...]}.
    """
    first_eps, last_eps = eps[0], eps[-1]
    if first_eps < 0 or last_eps < 0:
        return {"error": "Cannot project future market price due to Negative EPS (DO NOT BUY)"}
    if first_eps < last_eps:
        return {"error": "Earnings is going down (DO NOT BUY)"}
    if min(eps) < 0:
        return {"error": "Negative EPS detected, earnings may not be consistent (DO NOT BUY)"}

    avg_eps_growth = ((first_eps / last_eps) ** (1 / len(eps))) - 1
    avg_pe = sum(pe) / len(pe)

    ten_year_eps = round(((1 + avg_eps_growth) ** 10) * first_eps, 2)
    ten_year_market_price = round(ten_year_eps * avg_pe, 2)
    ten_year_max_market_price = round(ten_year_eps * max(pe), 2)
    ten_year_min_market_price = round(ten_year_eps * min(pe), 2)
    annual_growth_rate = round((((ten_year_market_price / price) ** 0.1) - 1) * 100, 2)
    max_growth_rate = round((((ten_year_max_market_price / price) ** 0.1) - 1) * 100, 2)
    min_growth_rate = round((((ten_year_min_market_price / price) ** 0.1) - 1) * 100, 2)

    return {"rows": [
        {"label": "Current Price",            "value": price,                    "color": None},
        {"label": "EPS in 10 years",           "value": ten_year_eps,             "color": None},
        {"label": "Market Price in 10 years",  "value": ten_year_market_price,    "color": None},
        {"label": "Max Market Price",          "value": ten_year_max_market_price,"color": None},
        {"label": "Min Market Price",          "value": ten_year_min_market_price,"color": None},
        {"label": "Annual Growth Rate",        "value": annual_growth_rate,       "color": get_colour_class(annual_growth_rate, 2, 5, 0)},
        {"label": "Max Growth Rate",           "value": max_growth_rate,          "color": get_colour_class(max_growth_rate, 5, 8, 0)},
        {"label": "Min Growth Rate",           "value": min_growth_rate,          "color": get_colour_class(min_growth_rate, 0, 2, 0)},
    ]}
