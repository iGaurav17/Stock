# filename: stock_evaluator.py
import yfinance as yf

def evaluate_stock(ticker_symbol):
    stock = yf.Ticker(ticker_symbol)
    info = stock.info

    print(f"\n📊 Evaluating: {info.get('shortName')} ({ticker_symbol})")

    try:
        pe_ratio = info.get("trailingPE", 0)
        roe = info.get("returnOnEquity", 0) * 100  # It's usually in decimal
        debt_equity = info.get("debtToEquity", 0)
        market_cap = info.get("marketCap", 0)
        sector = info.get("sector", "Unknown")

        print(f"Sector: {sector}")
        print(f"P/E Ratio: {pe_ratio}")
        print(f"ROE: {roe:.2f}%")
        print(f"Debt to Equity: {debt_equity}")
        print(f"Market Cap: ₹{market_cap / 1e7:.2f} Cr")

        # --- Scoring or Rule Based Logic ---
        if roe > 15 and pe_ratio < 30 and debt_equity < 1:
            print("✅ Recommendation: BUY (Strong Fundamentals)")
            if pe_ratio < 15:
                reason = "Undervalued with low P/E ratio"
            elif roe > 20:
                reason = "High return on equity (ROE)"
            elif debt_equity < 0.5:
                reason = "Very low debt, financially safe"
        elif roe < 10 or debt_equity > 2:
            print("❌ Recommendation: AVOID (Weak financials)")
            if roe < 10:
                reason = "Low return on equity (ROE)"
            elif debt_equity > 2:
                reason = "High debt-to-equity ratio"
            elif pe_ratio > 50:
                reason = "Overvalued based on P/E ratio"
        else:
            print("⚠️ Recommendation: WATCH (Moderate metrics)")
            if 10 <= roe <= 15:
                reason = "Average ROE, room for improvement"
            elif 1 <= debt_equity <= 2:
                reason = "Moderate debt levels"
            else:
                reason = "No clear signal, monitor performance"

        print(f"📌 Reason: {reason}")
    except Exception as e:
        print("Error fetching data:", e)

# Example
if __name__ == "__main__":
    ticker_input = input("Enter Indian Stock Ticker (e.g., INFY.NS): ").strip().upper()
    evaluate_stock(ticker_input)

