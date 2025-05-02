from sklearn.linear_model import LinearRegression
import numpy as np
import yfinance as yf
from datetime import timedelta
import matplotlib.pyplot as plt
import pandas as pd
from prophet import Prophet
import streamlit as st
# def predict_with_linear_regression(ticker):
#     stock = yf.Ticker(ticker)
#     history = stock.history(period="6mo")

#     if history.empty:
#         print("Not enough data for prediction.")
#         return

#     df = history.reset_index()[["Date", "Close"]]
#     df['Date'] = pd.to_datetime(df['Date'])
#     df['ds'] = df['Date'].map(pd.Timestamp.toordinal)  # Convert dates to ordinal numbers
#     df['y'] = df['Close']

#     # Prepare training data
#     X = df['ds'].values.reshape(-1, 1)
#     y = df['y'].values

#     # Train the model
#     model = LinearRegression()
#     model.fit(X, y)

#     # Generate next 7 days
#     last_date = df['Date'].max()
#     future_dates = [last_date + timedelta(days=i) for i in range(1, 8)]
#     future_ordinals = np.array([date.toordinal() for date in future_dates]).reshape(-1, 1)
#     future_preds = model.predict(future_ordinals)

#     # Combine actual and predicted
#     all_dates = list(df['Date']) + future_dates
#     all_prices = list(df['y']) + list(future_preds)

#     # Plot
#     plt.figure(figsize=(12, 5))
#     plt.plot(df['Date'], df['y'], label="Historical Prices", marker='o')
#     plt.plot(future_dates, future_preds, label="Predicted Prices (Next 7 Days)", marker='x', linestyle='--', color='orange')
#     plt.axvline(x=last_date, linestyle='--', color='gray', label='Prediction Starts')
#     plt.title(f"📈 Linear Regression Price Forecast for {ticker.upper()} - Next 7 Days")
#     plt.xlabel("Date")
#     plt.ylabel("Price (INR)")
#     plt.xticks(rotation=45)
#     plt.grid(True)
#     plt.legend()
#     plt.tight_layout()
#     st.pyplot(plt.gcf())
def predict_detailed_7day_forecast(ticker):
    stock = yf.Ticker(ticker)
    history = stock.history(period="6mo")

    if history.empty:
        print("Not enough historical data.")
        return

    df = history.reset_index()[["Date", "Close"]]
    df.rename(columns={"Date": "ds", "Close": "y"}, inplace=True)
    df['ds'] = df['ds'].dt.tz_localize(None)  # remove timezone

    model = Prophet(daily_seasonality=True, interval_width=0.95)
    model.fit(df)

    future = model.make_future_dataframe(periods=7)
    forecast = model.predict(future)

    # Filter next 7 days forecast only
    last_date = df['ds'].max()
    future_forecast = forecast[forecast['ds'] > last_date]

    # Plot
    plt.figure(figsize=(12, 5))
    plt.plot(df['ds'], df['y'], label="Historical", color="blue")
    plt.plot(future_forecast['ds'], future_forecast['yhat'], label="Predicted", color="orange", marker='o')
    plt.fill_between(future_forecast['ds'], future_forecast['yhat_lower'], future_forecast['yhat_upper'], color='orange', alpha=0.2, label="High/Low Range")

    for i in range(len(future_forecast)):
        ds = future_forecast['ds'].iloc[i].strftime("%b %d")
        high = round(future_forecast['yhat_upper'].iloc[i], 2)
        low = round(future_forecast['yhat_lower'].iloc[i], 2)
        plt.text(future_forecast['ds'].iloc[i], future_forecast['yhat'].iloc[i] + 2, f"H:{high}", color='green', fontsize=9, ha='center')
        plt.text(future_forecast['ds'].iloc[i], future_forecast['yhat'].iloc[i] - 2, f"L:{low}", color='red', fontsize=9, ha='center')

    plt.axvline(x=last_date, linestyle='--', color='gray', label='Forecast Start')
    plt.title(f"📈 7-Day Forecast with High/Low Bands for {ticker.upper()}")
    plt.xlabel("Date")
    plt.ylabel("Price (INR)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.xticks(rotation=45)
    st.pyplot(plt.gcf())
def show_chart(metrics, ticker):
    if not metrics:
        st.warning("No data to visualize.")
        return

    stock = yf.Ticker(ticker)
    labels = list(metrics.keys())
    values = list(metrics.values())
    history = stock.history(period="30d")
    recent_history = history.tail(30)
    intraday_data = stock.history(period="1d", interval="1m")

    fig, axs = plt.subplots(3, 1, figsize=(12, 12))

    # Bar chart
    axs[0].bar(labels, values, color='skyblue', edgecolor='black')
    axs[0].set_title(f"📈 Contribution to Score for {ticker}")
    axs[0].set_ylabel("Score Contribution")
    axs[0].grid(axis='y', linestyle='--', alpha=0.6)

    # 30-day trend
    if not recent_history.empty:
        axs[1].plot(recent_history.index, recent_history["Close"], marker='o')
        axs[1].set_title(f"{ticker.upper()} - Last 30 Days Closing Price")
        axs[1].set_ylabel("Price (INR)")
        axs[1].grid(True)
    else:
        axs[1].set_title("No recent history data found")
        axs[1].axis('off')

    # Intraday data
    if not intraday_data.empty:
        axs[2].plot(intraday_data.index, intraday_data["Close"], color='green')
        axs[2].set_title(f"{ticker.upper()} - Intraday Price Movement")
        axs[2].tick_params(axis='x', rotation=45)
        axs[2].grid(True)
    else:
        axs[2].set_title("No intraday data found")
        axs[2].axis('off')

    fig.tight_layout()
    st.pyplot(fig)  # ✅ Explicitly show your first figure

    # Then call forecast (which draws its own figure)
    predict_detailed_7day_forecast(ticker)  # This will have its own plot