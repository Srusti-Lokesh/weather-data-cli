"""Small Flask web interface so the project can be deployed as a Render Web Service."""
import os
from flask import Flask, render_template, request
from weather_cli import fetch_weather, WeatherError

app = Flask(__name__)

@app.get("/")
def home():
    return render_template("index.html", weather=None, error=None, city="")

@app.get("/weather")
def weather():
    city = request.args.get("city", "").strip()
    if not city:
        return render_template("index.html", weather=None, error="Enter a city name.", city=city), 400
    try:
        result = fetch_weather(city, os.getenv("OPENWEATHER_API_KEY", "").strip())
        return render_template("index.html", weather=result, error=None, city=city)
    except WeatherError as exc:
        return render_template("index.html", weather=None, error=str(exc), city=city), 400

@app.get("/health")
def health():
    return {"status": "ok"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=False)
