import streamlit as st
import pandas as pd
from historical import get_historical_data, get_historical_data_header
from projections import calc_projections
from fundamentals import calc_fundamentals

st.set_page_config(page_title="Value Investing Analysis", layout="wide")
st.title("Value Investing Analysis")

search_col, _ = st.columns([1, 3])
with search_col:
    with st.form("search"):
        input_col, btn_col = st.columns([3, 1])
        ticker = input_col.text_input("Ticker", placeholder="e.g. AAPL", label_visibility="collapsed").upper().strip()
        analyze = btn_col.form_submit_button("Analyze")

COLOR_CSS = {
    "green":  "background-color: #d4edda; color: #155724",
    "yellow": "background-color: #fff3cd; color: #856404",
    "red":    "background-color: #f8d7da; color: #721c24",
}

def _highlight(colors):
    def apply(row):
        css = COLOR_CSS.get(colors[row.name], "")
        return [css] * len(row)
    return apply

def display_colored_table(rows):
    df = pd.DataFrame({"Metric": [r["label"] for r in rows], "Value": [r["value"] for r in rows]})
    colors = [r.get("color") for r in rows]
    styled = df.style.apply(_highlight(colors), axis=1).set_properties(**{"text-align": "left"})
    st.dataframe(styled, use_container_width=True, hide_index=True)

if analyze and ticker:
    with st.status("Fetching data for {}...".format(ticker), expanded=True) as status:
        try:
            eps, pe_ratio, financial_data = get_historical_data(ticker, log=st.write)
        except Exception as e:
            status.update(label=str(e), state="error")
            st.stop()
        status.update(label="Data fetched", state="complete", expanded=False)

    header = get_historical_data_header()
    result = calc_projections(eps, pe_ratio, financial_data.get_price())

    col_eps, col_pe, col_proj, col_fund = st.columns(4)

    with col_eps:
        st.subheader("EPS (10yr)")
        st.dataframe(
            pd.DataFrame({"Year": header, "EPS": eps}),
            use_container_width=True,
            hide_index=True,
        )
    with col_pe:
        st.subheader("PE Ratio (10yr)")
        st.dataframe(
            pd.DataFrame({"Year": header, "PE Ratio": pe_ratio}),
            use_container_width=True,
            hide_index=True,
        )
    with col_proj:
        st.subheader("Projections")
        if "error" in result:
            st.error(result["error"])
        else:
            display_colored_table(result["rows"])
    with col_fund:
        st.subheader("Financial Ratios")
        display_colored_table(calc_fundamentals(financial_data))
