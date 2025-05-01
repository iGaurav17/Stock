def interpret_pe(pe_ratio):
    if pe_ratio is None: return "P/E ratio not available."
    if pe_ratio < 15: return "✅ Undervalued: Stock may be trading at a bargain."
    if pe_ratio <= 30: return "ℹ️ Fairly valued: In a normal range."
    if pe_ratio <= 50: return "⚠️ Slightly Overvalued."
    return "❌ Highly Overvalued."

def interpret_eps(eps):
    if eps is None: return "EPS not available."
    if eps >= 50: return "✅ Strong earnings per share."
    if eps >= 10: return "ℹ️ Decent earnings per share."
    if eps > 0: return "⚠️ Low EPS."
    return "❌ Negative or Zero EPS."

def interpret_roe(roe):
    if roe is None: return "ROE not available."
    roe *= 100
    if roe >= 25: return "✅ Excellent ROE."
    if roe >= 15: return "ℹ️ Good ROE."
    if roe >= 5: return "⚠️ Below average ROE."
    return "❌ Poor ROE."

def interpret_dividend_yield(dy):
    if dy is None: return "Dividend yield not available."
    dy *= 100
    if dy >= 5: return "✅ High dividend."
    if dy >= 2: return "ℹ️ Reasonable yield."
    if dy > 0: return "⚠️ Low dividend yield."
    return "❌ No dividends paid."

def interpret_profit_margin(pm):
    if pm is None: return "Profit margin not available."
    pm *= 100
    if pm >= 20: return "✅ High margin."
    if pm >= 10: return "ℹ️ Moderate margin."
    if pm > 0: return "⚠️ Low margin."
    return "❌ Negative margin."

def interpret_debt_equity(de):
    if de is None: return "Debt-equity ratio not available."
    if de < 0.5: return "✅ Very low debt."
    if de <= 1.5: return "ℹ️ Moderate debt."
    if de <= 2.5: return "⚠️ High debt."
    return "❌ Very high debt."