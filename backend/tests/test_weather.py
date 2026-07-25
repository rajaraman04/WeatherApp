from datetime import date, datetime, timedelta
import pytest
from fastapi.testclient import TestClient
from app.config import Settings, get_settings
from app.exceptions import ExternalAPIError
from app.main import app
from app.routes import weather as weather_route
from app.schemas import WeatherQuery
from app.services.weather_service import parse_weather_response, weather_code_to_condition

client = TestClient(app)

@pytest.fixture(autouse=True)
def override_settings():
    test_settings= Settings(mongodb_uri="mongodb://test",)
    app.dependency_overrides[get_settings]= (lambda: test_settings)
    yield
    app.dependency_overrides.clear()

def create_sample_api_response(start_date:date,):
    second_date = start_date + timedelta(days=1)
    return {"latitude": 42.1,"longitude": -75.9,"timezone": "America/New_York","timezone_abbreviation": "EDT",
        "current": {"time": (f"{start_date.isoformat()}T12:00"),
        "temperature_2m": 78.5,"apparent_temperature": 80.2,"relative_humidity_2m": 65,"precipitation": 0,"weather_code": 2,"wind_speed_10m": 7.5,"is_day": 1,},
        "daily": {"time": [start_date.isoformat(),second_date.isoformat(),],
            "weather_code": [2, 61],
            "temperature_2m_max": [82.0, 76.0],
            "temperature_2m_min": [64.0, 62.0],
            "precipitation_probability_max": [20,70,],
            "precipitation_sum": [0.0, 0.4],
            "wind_speed_10m_max": [12.0, 14.0],
            "sunrise": [f"{start_date.isoformat()}T05:50",f"{second_date.isoformat()}T05:51",],
            "sunset": [f"{start_date.isoformat()}T20:30",f"{second_date.isoformat()}T20:29",],
        },
    }

def test_weather_code_to_condition():
    assert weather_code_to_condition(0)== "Clear sky"
    assert weather_code_to_condition(61)== "Slight rain"
    assert weather_code_to_condition(999)== "Unknown"
    assert weather_code_to_condition(None)== "Unknown"


def test_parse_weather_response():
    today = date.today()
    tomorrow = today + timedelta(days=1)
    query = WeatherQuery(latitude=42.0987,longitude=-75.9180,start_date=today,end_date=tomorrow,temperature_unit="fahrenheit",)
    result = parse_weather_response(create_sample_api_response(today),query,)
    assert result.timezone== "America/New_York"
    assert result.current_weather.temperature== 78.5
    assert result.current_weather.condition== "Partly cloudy"
    assert len(result.forecast)== 2
    assert result.forecast[1].condition== "Slight rain"
    assert result.wind_speed_unit== "mph"


def test_weather_endpoint_returns_weather(monkeypatch,):
    today = date.today()
    tomorrow = today + timedelta(days=1)
    async def fake_fetch_weather(query,settings,):
        return parse_weather_response(create_sample_api_response(today),query,)
    monkeypatch.setattr(weather_route,"fetch_weather",fake_fetch_weather,)
    response = client.get("/api/weather",
        params={"latitude":42.0987,"longitude":-75.9180,"start_date": today.isoformat(),"end_date": tomorrow.isoformat(),"temperature_unit": "fahrenheit",},)

    assert response.status_code==200
    response_data = response.json()

    assert response_data["timezone"] == ("America/New_York")
    assert response_data["current_weather"]["condition"] == "Partly cloudy"
    assert len(response_data["forecast"])==2

def test_weather_endpoint_handles_api_failure(monkeypatch,):
    today = date.today()
    async def fake_fetch_weather(query,settings,):
        raise ExternalAPIError("The weather service could not be reached.")
    monkeypatch.setattr(weather_route,"fetch_weather",fake_fetch_weather,)
    response = client.get("/api/weather",params={"latitude": 42.0987,"longitude": -75.9180,"start_date": today.isoformat(),"end_date": today.isoformat(),"temperature_unit": "fahrenheit",},)
    assert response.status_code==502
    assert response.json()== {"detail": ("The weather service could not be reached.")}

def test_weather_endpoint_rejects_invalid_latitude():
    today = date.today()
    response = client.get("/api/weather",params={"latitude": 100,"longitude": -75.9180,"start_date": today.isoformat(),"end_date": today.isoformat(),"temperature_unit": "fahrenheit",},)
    assert response.status_code==422

def test_weather_endpoint_rejects_long_date_range():
    today=date.today()
    end_date= today + timedelta(days=5)
    response = client.get("/api/weather",params={"latitude": 42.0987,"longitude": -75.9180,"start_date": today.isoformat(),"end_date": end_date.isoformat(),"temperature_unit": "fahrenheit",},)
    assert response.status_code==422