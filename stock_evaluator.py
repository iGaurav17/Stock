import yfinance as yf

def evaluate_stock(ticker_symbol):
    stock = yf.Ticker(ticker_symbol)
    info = stock.info

    print(f"\n📊 Evaluating: {info.get('shortName')} ({ticker_symbol})")

    try:
        pe_ratio = info.get("trailingPE", None)
        roe = info.get("returnOnEquity", None)
        debt_equity = info.get("debtToEquity", None)
        market_cap = info.get("marketCap", 0)
        sector = info.get("sector", "Unknown")

        print(f"Sector: {sector}")
        print(f"P/E Ratio: {pe_ratio}")
        print(f"ROE: {roe * 100 if roe else 'N/A'}%")
        print(f"Debt to Equity: {debt_equity}")
        print(f"Market Cap: ₹{market_cap / 1e7:.2f} Cr")

        # --- Profitability Scoring ---
        score = 50  # base score

        # ROE scoring
        if roe is not None:
            roe *= 100
            if roe >= 25:
                score += 30
            elif roe >= 15:
                score += 20
            elif roe >= 10:
                score += 10
            elif roe < 5:
                score -= 15  # penalty for poor ROE

        # PE ratio scoring
        if pe_ratio is not None:
            if pe_ratio < 15:
                score += 10
            elif 15 <= pe_ratio <= 30:
                score += 5
            elif pe_ratio > 50:
                score -= 10  # overvalued

        # Debt to equity scoring
        if debt_equity is not None:
            if debt_equity < 0.5:
                score += 10
            elif 0.5 <= debt_equity <= 1.5:
                score += 5
            elif debt_equity > 2:
                score -= 15  # high debt risk

        # Clamp score between -50 and 100
        score = max(-50, min(score, 100))

        # Convert to "profit chance" style metric
        if score >= 70:
            verdict = "🚀 High potential"
        elif 40 <= score < 70:
            verdict = "⚖️ Moderate"
        elif 10 <= score < 40:
            verdict = "⚠️ Risky"
        else:
            verdict = "❌ Avoid"

        print(f"\n📈 Estimated Profitability Score: {score}% ({verdict})")

    except Exception as e:
        print("Error fetching data:", e)

# Example
if __name__ == "__main__":
    ticker_input = input("Enter Indian Stock Ticker (e.g., INFY.NS): ").strip().upper()
    evaluate_stock(ticker_input)