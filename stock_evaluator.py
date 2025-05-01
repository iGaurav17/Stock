import yfinance as yf  # Yahoo Finance API to fetch stock data
import matplotlib.pyplot as plt
import mplfinance as mpf

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


        # ✅ Add this block: fetch last 5 days history and print
        history = stock.history(period="30d")
        if not history.empty:
            print("\n📅 Last 30 days closing prices:")
            print(history["Close"])

            # ✅ Plotting the chart
            history["Close"].plot(title=f"{ticker.upper()} - Last 5 Days Closing Price", figsize=(10, 4), marker='o')
            plt.ylabel("Price (INR)")
            plt.xlabel("Date")
            plt.grid(True)
            plt.tight_layout()
            plt.show(block=False)
            plt.pause(3)  # Pause for 3 seconds to allow the plot to render
        else:
            print("⚠️ No historical price data found.")


        intraday_data = stock.history(period="1d", interval="1m")  # 1-day data with 5-minute intervals
        if not intraday_data.empty:
            print("\n📅 Intraday Price (1-minute intervals):")
            print(intraday_data[["Close"]].tail())

            # Plot intraday price chart
            plt.figure(figsize=(12, 5))
            plt.plot(intraday_data.index, intraday_data["Close"], marker='', linestyle='-', color='green')
            plt.title(f"{ticker.upper()} - Intraday Price Movement (5-minute intervals)")
            plt.xlabel("Time")
            plt.ylabel("Price (INR)")
            plt.xticks(rotation=45)
            plt.grid(True, linestyle='--', alpha=0.5)
            plt.tight_layout()
            plt.show(block=False)
            plt.pause(3)  # Pause for 3 seconds to allow the plot to render
        else: 
            print("⚠️ Intraday price data not available.")

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

# Visualization function
def show_chart(metrics, ticker):
    if not metrics:
        print("No data to visualize.")
        return

    labels = list(metrics.keys())
    values = list(metrics.values())

    plt.figure(figsize=(10, 5))
    bars = plt.bar(labels, values, color='skyblue', edgecolor='black')
    plt.title(f"📈 Contribution to Score for {ticker}")
    plt.ylabel("Score Contribution")
    plt.grid(axis='y', linestyle='--', alpha=0.6)

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.5, f"{yval}", ha='center', va='bottom')

    plt.show()
    # plt.show(block=False)
    # plt.pause(3)  # Pause for 3 seconds to allow the plot to render

# Interpretation helpers
def interpret_pe(pe_ratio):
    if pe_ratio is None:
        return "P/E ratio not available."
    elif pe_ratio < 15:
        return "✅ Undervalued: Stock may be trading at a bargain."
    elif 15 <= pe_ratio <= 30:
        return "ℹ️ Fairly valued: In a normal valuation range."
    elif pe_ratio <= 50:
        return "⚠️ Slightly Overvalued: Priced higher relative to earnings."
    else:
        return "❌ Highly Overvalued: Market has high expectations or earnings are very low."

def interpret_eps(eps):
    if eps is None:
        return "EPS not available."
    elif eps >= 50:
        return "✅ Strong earnings per share. Company is very profitable."
    elif eps >= 10:
        return "ℹ️ Decent earnings per share."
    elif eps > 0:
        return "⚠️ Low EPS: Company is profitable but earnings are low."
    else:
        return "❌ Negative or Zero EPS: Company may be losing money."

def interpret_roe(roe):
    if roe is None:
        return "ROE not available."
    roe *= 100
    if roe >= 25:
        return "✅ Excellent return on equity."
    elif roe >= 15:
        return "ℹ️ Good ROE: Management is using capital efficiently."
    elif roe >= 5:
        return "⚠️ Below average ROE."
    else:
        return "❌ Poor ROE: Inefficient capital usage."

def interpret_dividend_yield(dy):
    if dy is None:
        return "Dividend yield not available."
    dy *= 100
    if dy >= 5:
        return "✅ High dividend: Attractive for income-focused investors."
    elif dy >= 2:
        return "ℹ️ Reasonable dividend yield."
    elif dy > 0:
        return "⚠️ Low dividend yield."
    else:
        return "❌ No dividends paid."

def interpret_profit_margin(pm):
    if pm is None:
        return "Profit margin not available."
    pm *= 100
    if pm >= 20:
        return "✅ High profit margin: Excellent cost control."
    elif pm >= 10:
        return "ℹ️ Moderate profit margin."
    elif pm > 0:
        return "⚠️ Low margin: Tight profit space."
    else:
        return "❌ Negative margin: Company is not profitable."

def interpret_debt_equity(de):
    if de is None:
        return "Debt-equity ratio not available."
    if de < 0.5:
        return "✅ Very low debt: Financially safe."
    elif de <= 1.5:
        return "ℹ️ Moderate debt levels."
    elif de <= 2.5:
        return "⚠️ High debt: Needs monitoring."
    else:
        return "❌ Very high debt: Financial risk is significant."

# Main entry
if __name__ == "__main__":
    ticker = input("Enter Indian Stock Ticker (e.g., INFY.NS): ")
    evaluate_stock(ticker)