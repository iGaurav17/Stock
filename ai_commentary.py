# ai_commentary.py

import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

models = genai.list_models()
for model in models:
    print(model.name, model.supported_generation_methods)

def generate_ai_commentary(ticker, future_forecast):
    if future_forecast.empty:
        return "Not enough forecast data for commentary."

    avg_price = future_forecast["yhat"].mean()
    trend = "upward 📈" if future_forecast["yhat"].iloc[-1] > future_forecast["yhat"].iloc[0] else "downward 📉"

    prompt = f"""
    Based on the 7-day forecast for stock ticker {ticker.upper()}, the predicted average price is around ₹{avg_price:.2f}, showing a likely {trend} trend.
    Write a short, engaging stock market commentary for this trend in less than 80 words.
    """

    try:
        model = genai.GenerativeModel(model_name="models/gemini-1.5-pro")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"❌ Error generating commentary: {str(e)}"