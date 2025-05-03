import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Error generating commentary: {str(e)}"