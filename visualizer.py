import yfinance as yf
import matplotlib.pyplot as plt

def show_chart(metrics, ticker):
    if not metrics:
        print("No data to visualize.")
        return

    stock = yf.Ticker(ticker)
    labels = list(metrics.keys())
    values = list(metrics.values())
    history = stock.history(period="30d")
    recent_history = history.tail(30)
    intraday_data = stock.history(period="1d", interval="1m")

    fig, axs = plt.subplots(3, 1, figsize=(12, 12))

    axs[0].bar(labels, values, color='skyblue', edgecolor='black')
    axs[0].set_title(f"📈 Contribution to Score for {ticker}")
    axs[0].set_ylabel("Score Contribution")
    axs[0].grid(axis='y', linestyle='--', alpha=0.6)

    if not recent_history.empty:
        axs[1].plot(recent_history.index, recent_history["Close"], marker='o')
        axs[1].set_title(f"{ticker.upper()} - Last 30 Days Closing Price")
        axs[1].set_ylabel("Price (INR)")
        axs[1].grid(True)
    else:
        axs[1].set_title("No recent history data found")
        axs[1].axis('off')

    if not intraday_data.empty:
        axs[2].plot(intraday_data.index, intraday_data["Close"], color='green')
        axs[2].set_title(f"{ticker.upper()} - Intraday Price Movement")
        axs[2].tick_params(axis='x', rotation=45)
        axs[2].grid(True)
    else:
        axs[2].set_title("No intraday data found")
        axs[2].axis('off')

    plt.tight_layout()
    plt.show()