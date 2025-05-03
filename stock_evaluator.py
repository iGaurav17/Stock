import yfinance as yf
from interpreters import *
from visualizer import show_chart

def evaluate_stock(ticker_symbol):
    stock = yf.Ticker(ticker_symbol)
    info = stock.info

    result = {}

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

        # Score calculation
        score = 50
        metric_scores = {}

        if roe is not None:
            roe *= 100
            if roe >= 25: score += 30; metric_scores['ROE'] = 30 
            elif roe >= 15: score += 20; metric_scores['ROE'] = 20
            elif roe >= 10: score += 10; metric_scores['ROE'] = 10
            elif roe < 5: score -= 15; metric_scores['ROE'] = -15

        if pe_ratio is not None:
            if pe_ratio < 15: score += 10; metric_scores['P/E'] = 10
            elif 15 <= pe_ratio <= 30: score += 5; metric_scores['P/E'] = 5
            elif pe_ratio > 50: score -= 10; metric_scores['P/E'] = -10 

        if debt_equity is not None:
            if debt_equity < 0.5: score += 10; metric_scores['D/E'] = 10
            elif debt_equity <= 1.5: score += 5; metric_scores['D/E'] = 5
            elif debt_equity > 2: score -= 15; metric_scores['D/E'] = -15

        if eps is not None:
            if eps >= 50: score += 10; metric_scores['EPS'] = 10
            elif eps >= 20: score += 5; metric_scores['EPS'] = 5
            else: metric_scores['EPS'] = 0

        if dividend_yield is not None:
            dividend_yield *= 100
            if dividend_yield >= 2: score += 5; metric_scores['Dividend'] = 5
            elif dividend_yield >= 1: score += 2; metric_scores['Dividend'] = 2
            else: metric_scores['Dividend'] = 0

        if profit_margin is not None:
            profit_margin *= 100
            if profit_margin >= 20: score += 10; metric_scores['Margin'] = 10
            elif profit_margin >= 10: score += 5; metric_scores['Margin'] = 5
            else: metric_scores['Margin'] = 0

        score = max(-50, min(score, 100))

        if score >= 70: verdict = "🚀 High potential"
        elif 40 <= score < 70: verdict = "⚖️ Moderate"
        elif 10 <= score < 40: verdict = "⚠️ Risky"
        else: verdict = "❌ Avoid"

        result = {
            "name": info.get("shortName", ticker_symbol),
            "sector": sector,
            "market_cap": market_cap,
            "current_price": current_price,
            "pe_ratio": pe_ratio,
            "eps": eps,
            "roe": roe,
            "dividend_yield": dividend_yield,
            "profit_margin": profit_margin,
            "debt_equity": debt_equity,
            "score": score,
            "verdict": verdict,
            "metric_scores": metric_scores
        }

        return result
    
    except Exception as e:
        return {"error": f"Error fetching data: {e}"}