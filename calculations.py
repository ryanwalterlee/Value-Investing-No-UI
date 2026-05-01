import subprocess
import sys
from projections import calc_projections
from fundamentals import calc_fundamentals
from historical import get_historical_data, get_historical_data_header
from text_format import bold_text
from tabulate import tabulate

def run_cli():
    print()
    ticker = input(bold_text("Enter Ticker: ")).upper().strip()
    print()

    eps, pe_ratio, financial_data = get_historical_data(ticker, log=print)

    header = get_historical_data_header()

    print(bold_text("Past 10 years EPS"))
    print(tabulate([header, eps], headers="firstrow", tablefmt="grid"))
    print()

    print(bold_text("Past 10 years PE ratio"))
    print(tabulate([header, pe_ratio], headers="firstrow", tablefmt="grid"))
    print()

    print(bold_text("Projections based on Past EPS and PE Ratios"))
    result = calc_projections(eps, pe_ratio, financial_data.get_price())
    if "error" in result:
        print(bold_text(result["error"]))
    else:
        COLOR_MAP = {"green": "\033[1;32m", "yellow": "\033[1;33m", "red": "\033[1;31m"}
        RESET = "\033[0m"
        rows = [["Projections", "Values"]]
        for r in result["rows"]:
            color = COLOR_MAP.get(r["color"], "")
            value = "{}{}{}".format(color, r["value"], RESET) if r["color"] else r["value"]
            rows.append([r["label"], value])
        print(tabulate(rows, headers="firstrow", tablefmt="grid"))
    print()

    print(bold_text("Financial Soundness of Company based on Financial Ratios"))
    COLOR_MAP = {"green": "\033[1;32m", "yellow": "\033[1;33m", "red": "\033[1;31m"}
    RESET = "\033[0m"
    rows = [["Ratio", "Value"]]
    for r in calc_fundamentals(financial_data):
        color = COLOR_MAP.get(r["color"], "")
        value = "{}{}{}".format(color, r["value"], RESET) if r["color"] else r["value"]
        rows.append([r["label"], value])
    print(tabulate(rows, headers="firstrow", tablefmt="grid"))
    print()

def run_ui():
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])

print()
print("1. CLI")
print("2. UI  (opens in browser)")
print()
choice = input(bold_text("Select mode [1/2]: ")).strip()
print()

if choice == "2":
    run_ui()
else:
    run_cli()
