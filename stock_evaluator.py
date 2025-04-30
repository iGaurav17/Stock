import yfinance as yf  # Yahoo Finance API to fetch stock data

# Function to evaluate a given stock based on financial ratios
def evaluate_stock(ticker_symbol):
    stock = yf.Ticker(ticker_symbol)  # Create a Ticker object
    info = stock.info  # Fetch stock metadata

    print(f"\n📊 Evaluating: {info.get('shortName')} ({ticker_symbol})")

    try:
        # Extract key financial indicators
        pe_ratio = info.get("trailingPE", None)           # Price-to-Earnings Ratio
        roe = info.get("returnOnEquity", None)            # Return on Equity (in decimal)
        debt_equity = info.get("debtToEquity", None)      # Debt-to-Equity Ratio
        market_cap = info.get("marketCap", 0)             # Market Capitalization
        sector = info.get("sector", "Unknown")            # Sector info

        # Display basic info
        print(f"Sector: {sector}")
        print(f"P/E Ratio: {pe_ratio}")
        print(f"ROE: {roe * 100 if roe else 'N/A'}%")
        print(f"Debt to Equity: {debt_equity}")
        print(f"Market Cap: ₹{market_cap / 1e7:.2f} Cr")

        # --- Custom Profitability Scoring ---
        score = 50  # Start with a neutral base score

        # Scoring based on ROE
        if roe is not None:
            roe *= 100  # Convert from decimal to percentage
            if roe >= 25:
                score += 30  # Excellent ROE
            elif roe >= 15:
                score += 20
            elif roe >= 10:
                score += 10
            elif roe < 5:
                score -= 15  # Poor ROE penalty

        # Scoring based on P/E Ratio
        if pe_ratio is not None:
            if pe_ratio < 15:
                score += 10  # Undervalued
            elif 15 <= pe_ratio <= 30:
                score += 5   # Fairly valued
            elif pe_ratio > 50:
                score -= 10  # Overvalued

        # Scoring based on Debt-to-Equity Ratio
        if debt_equity is not None:
            if debt_equity < 0.5:
                score += 10  # Financially stable
            elif 0.5 <= debt_equity <= 1.5:
                score += 5   # Acceptable debt
            elif debt_equity > 2:
                score -= 15  # Risky debt level

        # Clamp final score between -50 (very risky) and 100 (very strong)
        score = max(-50, min(score, 100))

        # Classify score into a human-readable verdict
        if score >= 70:
            verdict = "🚀 High potential"
        elif 40 <= score < 70:
            verdict = "⚖️ Moderate"
        elif 10 <= score < 40:
            verdict = "⚠️ Risky"
        else:
            verdict = "❌ Avoid"

        # Output the final profitability estimation
        print(f"\n📈 Estimated Profitability Score: {score}% ({verdict})")

    except Exception as e:
        print("Error fetching data:", e)

# Main driver block
if __name__ == "__main__":
    # Ask user to input stock ticker (e.g., INFY.NS for Infosys)
    ticker_input = input("Enter Indian Stock Ticker (e.g., INFY.NS): ").strip().upper()
    evaluate_stock(ticker_input)