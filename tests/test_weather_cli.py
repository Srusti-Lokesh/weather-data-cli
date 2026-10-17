import pytest
from unittest.mock import Mock
import weather_cli
from weather_cli import WeatherError, fetch_weather, format_weather

def test_fetch_weather_parses_response(monkeypatch):
    response = Mock()
    response.status_code = 200
    response.json.return_value = {
        "name": "Bengaluru", "sys": {"country": "IN"},
        "main": {"temp": 28.5, "feels_like": 30.0, "humidity": 60, "pressure": 1008},
        "weather": [{"description": "few clouds"}], "wind": {"speed": 3.2}
    }
    response.raise_for_status.return_value = None
    monkeypatch.setattr(weather_cli.requests, "get", Mock(return_value=response))
    result = fetch_weather("Bengaluru", "test-key")
    assert result["city"] == "Bengaluru"
    assert result["temperature"] == 28.5
    assert result["description"] == "Few clouds"

def test_missing_key():
    with pytest.raises(WeatherError, match="Missing API key"):
        fetch_weather("London", "")

def test_city_not_found(monkeypatch):
    response = Mock()
    response.status_code = 404
    monkeypatch.setattr(weather_cli.requests, "get", Mock(return_value=response))
    with pytest.raises(WeatherError, match="was not found"):
        fetch_weather("NoSuchCity", "test-key")

def test_format_weather():
    sample = {"city":"Bengaluru","country":"IN","temperature":28.5,"feels_like":30.0,
              "humidity":60,"description":"Clear sky","wind_speed":3.2,"pressure":1008}
    output = format_weather(sample)
    assert "28.5 °C" in output
    assert "Humidity" in output
