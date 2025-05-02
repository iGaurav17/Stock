import streamlit as st
from stock_evaluator import evaluate_stock
from visualizer import show_chart

st.set_page_config(page_title="📈 Stock Evaluator", layout="wide")

st.title("📊 Stock Score & Forecast App")
ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, INFY.NS)", value="AAPL")

if ticker:
    with st.spinner("Evaluating stock..."):
        result = evaluate_stock(ticker)

        if "error" in result:
            st.error(result["error"])
        else:
            metrics = result.get("metric_scores", {})
            verdict = result.get("verdict", "No verdict")

            st.subheader("📌 Verdict")
            st.success(verdict)

            st.subheader("📃 Details")
            st.write(f"**Name**: {result.get('name')}")
            st.write(f"**Sector**: {result.get('sector')}")
            st.write(f"**Market Cap**: {result.get('market_cap')}")
            st.write(f"**Current Price**: {result.get('current_price')}")
            st.write(f"**P/E Ratio**: {result.get('pe_ratio')}")
            st.write(f"**EPS**: {result.get('eps')}")
            st.write(f"**ROE**: {result.get('roe')}")
            st.write(f"**Dividend Yield**: {result.get('dividend_yield')}")
            st.write(f"**Profit Margin**: {result.get('profit_margin')}")
            st.write(f"**Debt/Equity**: {result.get('debt_equity')}")

            st.subheader("📉 Score Breakdown & Price Forecast")
            show_chart(metrics, ticker)

            st.subheader("🧠 AI Commentary")
            st.write(f"Based on recent trends, **{ticker.upper()}** is showing signs of...")

            