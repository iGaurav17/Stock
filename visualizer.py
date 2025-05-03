from sklearn.linear_model import LinearRegression
import numpy as np
import yfinance as yf
from datetime import timedelta
import pandas as pd
from prophet import Prophet
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from ai_commentary import generate_ai_commentary

def predict_detailed_7day_forecast(ticker):
    stock = yf.Ticker(ticker)
    history = stock.history(period="6mo")

    if history.empty:
        st.warning("Not enough historical data.")
        return None  # Important: return None if no data

    df = history.reset_index()[["Date", "Close"]]
    df.rename(columns={"Date": "ds", "Close": "y"}, inplace=True)
    df['ds'] = df['ds'].dt.tz_localize(None)

    model = Prophet(daily_seasonality=True, interval_width=0.95)
    model.fit(df)

    future = model.make_future_dataframe(periods=7)
    forecast = model.predict(future)

    last_date = df['ds'].max()
    future_forecast = forecast[forecast['ds'] > last_date]

    # Plot with Plotly
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df['ds'], y=df['y'], mode='lines+markers', name='Historical', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=future_forecast['ds'], y=future_forecast['yhat'], mode='lines+markers', name='Predicted', line=dict(color='orange')))

    fig.add_trace(go.Scatter(
        x=future_forecast['ds'],
        y=future_forecast['yhat_upper'],
        mode='lines',
        name='Upper Bound',
        line=dict(width=0),
        showlegend=False
    ))
    fig.add_trace(go.Scatter(
        x=future_forecast['ds'],
        y=future_forecast['yhat_lower'],
        mode='lines',
        name='Lower Bound',
        fill='tonexty',
        fillcolor='rgba(255,165,0,0.2)',
        line=dict(width=0),
        showlegend=True
    ))

    fig.update_layout(
        title=f"📈 7-Day Forecast with High/Low Bands for {ticker.upper()}",
        xaxis_title="Date",
        yaxis_title="Price (INR)",
        legend_title="Legend",
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)

    return future_forecast  # ✅ Return forecast for AI commentary


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

    # 1. Bar Chart for Metrics
    bar_fig = px.bar(
        x=labels,
        y=values,
        labels={'x': 'Metrics', 'y': 'Score Contribution'},
        title=f"📊 Contribution to Score for {ticker}",
        color=values,
        color_continuous_scale="Blues"
    )
    bar_fig.update_layout(yaxis=dict(gridcolor="lightgray"))

    st.plotly_chart(bar_fig, use_container_width=True)

    # 2. 30-day Price Trend
    if not recent_history.empty:
        price_fig = px.line(
            recent_history.reset_index(),
            x='Date',
            y='Close',
            title=f"{ticker.upper()} - Last 30 Days Closing Price",
            markers=True
        )
        st.plotly_chart(price_fig, use_container_width=True)
    else:
        st.info("No recent history data found.")

    # 3. Intraday Price Movement
    if not intraday_data.empty:
        intraday_fig = px.line(
            intraday_data.reset_index(),
            x='Datetime',
            y='Close',
            title=f"{ticker.upper()} - Intraday Price Movement"
        )
        st.plotly_chart(intraday_fig, use_container_width=True)
    else:
        st.info("No intraday data found.")

    # 4. Forecast and get future forecast data
    future_forecast = predict_detailed_7day_forecast(ticker)

    # 5. AI Commentary
    if future_forecast is not None:
        ai_comment = generate_ai_commentary(ticker, future_forecast)
        st.markdown("### 🧠 AI Commentary")
        st.success(ai_comment)
    else:
        st.info("AI commentary unavailable due to missing forecast.")