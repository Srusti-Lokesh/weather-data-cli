"""Command-line weather client using OpenWeatherMap's Current Weather API."""
import argparse
import os
import sys
import requests

API_URL = "https://api.openweathermap.org/data/2.5/weather"
TIMEOUT_SECONDS = 10

class WeatherError(Exception):
    """Expected, user-friendly weather lookup error."""

def fetch_weather(city: str, api_key: str) -> dict:
    if not city or not city.strip():
        raise WeatherError("Please provide a city name.")
    if not api_key:
        raise WeatherError("Missing API key. Set OPENWEATHER_API_KEY in your environment.")
    try:
        response = requests.get(
            API_URL,
            params={"q": city.strip(), "appid": api_key, "units": "metric"},
            timeout=TIMEOUT_SECONDS,
        )
    except requests.Timeout as exc:
        raise WeatherError("The weather service timed out. Please try again.") from exc
    except requests.RequestException as exc:
        raise WeatherError("Could not connect to the weather service. Check your internet connection.") from exc

    if response.status_code == 404:
        raise WeatherError(f"City '{city.strip()}' was not found. Check the spelling and try again.")
    if response.status_code == 401:
        raise WeatherError("The API key was rejected. Check OPENWEATHER_API_KEY and confirm the key is active.")
    if response.status_code == 429:
        raise WeatherError("The API rate limit was reached. Wait a while before trying again.")
    if response.status_code >= 500:
        raise WeatherError("The weather provider is temporarily unavailable. Try again later.")
    try:
        response.raise_for_status()
        data = response.json()
    except (requests.HTTPError, ValueError) as exc:
        raise WeatherError("The weather provider returned an unexpected response.") from exc

    try:
        return {
            "city": data["name"],
            "country": data.get("sys", {}).get("country", ""),
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"].capitalize(),
            "wind_speed": data["wind"]["speed"],
            "pressure": data["main"]["pressure"],
        }
    except (KeyError, IndexError, TypeError) as exc:
        raise WeatherError("The weather provider response was missing expected fields.") from exc

def format_weather(weather: dict) -> str:
    place = ", ".join(part for part in (weather["city"], weather["country"]) if part)
    return (
        f"\nWeather for {place}\n"
        f"{'─' * (12 + len(place))}\n"
        f"Conditions : {weather['description']}\n"
        f"Temperature: {weather['temperature']:.1f} °C\n"
        f"Feels like : {weather['feels_like']:.1f} °C\n"
        f"Humidity   : {weather['humidity']}%\n"
        f"Wind speed : {weather['wind_speed']} m/s\n"
        f"Pressure   : {weather['pressure']} hPa\n"
    )

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Get current weather for a city.")
    parser.add_argument("city", nargs="*", help="City name, e.g. Bengaluru")
    args = parser.parse_args(argv)
    city = " ".join(args.city).strip()
    if not city:
        city = input("Enter city name: ").strip()
    try:
        weather = fetch_weather(city, os.getenv("OPENWEATHER_API_KEY", "").strip())
        print(format_weather(weather))
        return 0
    except WeatherError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
