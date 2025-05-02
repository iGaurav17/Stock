import yfinance as yf  # Yahoo Finance API to fetch stock data
from interpreters import *
from visualizer import show_chart 
# from visualizer import predict_future_prices

# Function to evaluate a given stock based on financial ratios
def evaluate_stock(ticker_symbol):
    stock = yf.Ticker(ticker_symbol)
    info = stock.info

    print(f"\n📊 Evaluating: {info.get('shortName')} ({ticker_symbol})")

    try:
        # Extract key financial indicators
        pe_ratio = info.get("trailingPE")
        current_price = info.get("currentPrice")
        roe = info.get("returnOnEquity")
        debt_equity = info.get("debtToEquity")
        eps = info.get("trailingEps")
        dividend_yield = info.get("dividendYield")
        profit_margin = info.get("profitMargins")
        market_cap = info.get("marketCap", 0)
        sector = info.get("sector", "Unknown")

        # Print basic info
        print(f"📁 Sector            : {sector}")
        print(f"💰 Market Cap        : ₹{market_cap / 1e7:.2f} Cr\n")
        print(f"💵 Current Price      : ₹{current_price}" if current_price else "💵 Current Price      : N/A")

        print(f"📈 P/E Ratio         : {pe_ratio:.2f}" if pe_ratio else "📈 P/E Ratio         : N/A")
        print(f"   {interpret_pe(pe_ratio)}\n")

        print(f"📊 EPS               : {eps}" if eps else "📊 EPS               : N/A")
        print(f"   {interpret_eps(eps)}\n")

        print(f"📊 ROE               : {roe * 100:.2f}%" if roe else "📊 ROE               : N/A")
        print(f"   {interpret_roe(roe)}\n")

        print(f"💸 Dividend Yield    : {dividend_yield * 100:.2f}%" if dividend_yield else "💸 Dividend Yield    : N/A")
        print(f"   {interpret_dividend_yield(dividend_yield)}\n")

        print(f"📉 Profit Margin     : {profit_margin * 100:.2f}%" if profit_margin else "📉 Profit Margin     : N/A")
        print(f"   {interpret_profit_margin(profit_margin)}\n")

        print(f"🏦 Debt to Equity    : {debt_equity:.2f}" if debt_equity else "🏦 Debt to Equity    : N/A")
        print(f"   {interpret_debt_equity(debt_equity)}")

        # --- Custom Profitability Scoring ---
        score = 50  # Start with a neutral base score
        metric_scores = {}

        # Scoring based on ROE
        if roe is not None:
            roe *= 100
            if roe >= 25: score += 30; metric_scores['ROE'] = 30 
            elif roe >= 15: score += 20; metric_scores['ROE'] = 20
            elif roe >= 10: score += 10; metric_scores['ROE'] = 10
            elif roe < 5: score -= 15; metric_scores['ROE'] = -15

        # P/E Ratio
        if pe_ratio is not None:
            if pe_ratio < 15: score += 10; metric_scores['P/E'] = 10
            elif 15 <= pe_ratio <= 30: score += 5; metric_scores['P/E'] = 5
            elif pe_ratio > 50: score -= 10; metric_scores['P/E'] = -10 

        # Debt-to-Equity
        if debt_equity is not None:
            if debt_equity < 0.5: score += 10; metric_scores['D/E'] = 10
            elif debt_equity <= 1.5: score += 5; metric_scores['D/E'] = 5
            elif debt_equity > 2: score -= 15; metric_scores['D/E'] = -15

        # EPS
        if eps is not None:
            if eps >= 50: score += 10; metric_scores['EPS'] = 10
            elif eps >= 20: score += 5; metric_scores['EPS'] = 5
            else: metric_scores['EPS'] = 0

        # Dividend Yield
        if dividend_yield is not None:
            dividend_yield *= 100
            if dividend_yield >= 2: score += 5; metric_scores['Dividend'] = 5
            elif dividend_yield >= 1: score += 2; metric_scores['Dividend'] = 2
            else: metric_scores['Dividend'] = 0

        # Profit Margin
        if profit_margin is not None:
            profit_margin *= 100
            if profit_margin >= 20: score += 10; metric_scores['Margin'] = 10
            elif profit_margin >= 10: score += 5; metric_scores['Margin'] = 5
            else: metric_scores['Margin'] = 0

        # Clamp score
        score = max(-50, min(score, 100))

        # Verdict
        if score >= 70: verdict = "🚀 High potential"
        elif 40 <= score < 70: verdict = "⚖️ Moderate"
        elif 10 <= score < 40: verdict = "⚠️ Risky"
        else: verdict = "❌ Avoid"

        # Move score display here (after calculations)
        print("\n" + "━" * 50)
        print(f"📈 Estimated Profitability Score: {score}% ({verdict})")
        print("━" * 50)

        # Visualization
        show_chart(metric_scores, ticker_symbol)

    except Exception as e:
        print("Error fetching data:", e)