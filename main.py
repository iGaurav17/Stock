from stock_evaluator import evaluate_stock


if __name__ == "__main__":
    ticker = input("Enter Indian Stock Ticker (e.g., INFY.NS): ")
    if ticker:
        evaluate_stock(ticker)
    else:
        print("Ticker symbol is required to proceed.")