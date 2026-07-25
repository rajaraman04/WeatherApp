from datetime import date, datetime, timezone
from types import SimpleNamespace
import pytest
from bson import ObjectId
from fastapi.testclient import TestClient
from pymongo.errors import ConnectionFailure
from app.config import Settings, get_settings
from app.exceptions import ExternalAPIError,LocationNotFoundError
from app.main import app
from app.routes import weather_records as records_route

client = TestClient(app)

@pytest.fixture(autouse=True)
def override_settings():
    test_settings = Settings(mongodb_uri="mongodb://test",)
    app.dependency_overrides[get_settings] = (lambda: test_settings)
    yield
    app.dependency_overrides.clear()


def sample_weather_document() -> dict:
    today = date.today()
    current_time = datetime.now(timezone.utc)
    return {
        "location_query": "Binghamton, NY",
        "resolved_location": {"name": "Binghamton","state": "New York","country": "United States","postal_code": "13901","latitude": 42.0987,"longitude": -75.9180,},
        "start_date": today.isoformat(),
        "end_date": today.isoformat(),
        "weather_source": "forecast",
        "temperature_unit": "fahrenheit",
        "wind_speed_unit": "mph",
        "precipitation_unit": "inch",
        "timezone": "America/New_York",
        "timezone_abbreviation": "EDT",
        "current_weather": {"temperature": 78.0,"condition": "Partly cloudy",},
        "forecast": [{"forecast_date": today.isoformat(),"minimum_temperature": 64.0,"maximum_temperature": 82.0,"condition": "Partly cloudy",}],
        "air_quality": None,"travel_insights": [],"created_at": current_time,"updated_at": current_time,
    }


class SuccessfulCollection:
    def __init__(self) -> None:
        self.saved_document = None

    async def insert_one(self, document):
        self.saved_document = document
        return SimpleNamespace(inserted_id=ObjectId())

class FailingCollection:
    async def insert_one(self, document):
        raise ConnectionFailure("Test database failure")

def test_create_weather_record(monkeypatch,):
    fake_collection = SuccessfulCollection()
    app.state.weather_collection = fake_collection

    async def fake_prepare_document(request_data,settings,):
        return sample_weather_document()

    monkeypatch.setattr(records_route,"prepare_weather_record_document",fake_prepare_document,)
    today = date.today()
    response = client.post("/api/weather-records",json={"location": "Binghamton, NY","start_date": today.isoformat(),"end_date": today.isoformat(),"temperature_unit": "fahrenheit",},)
    assert response.status_code == 201
    response_data = response.json()
    assert len(response_data["id"]) == 24
    assert response_data["location_query"] == ("Binghamton, NY")
    assert response_data["weather_source"] == ("forecast")
    assert fake_collection.saved_document is not None

def test_create_returns_404_for_unknown_location(monkeypatch,):
    async def fake_prepare_document(request_data,settings,):
        raise LocationNotFoundError(request_data.location)
    monkeypatch.setattr(records_route,"prepare_weather_record_document",fake_prepare_document,)
    today = date.today()
    response = client.post("/api/weather-records",json={"location": "UnknownPlace","start_date": today.isoformat(),"end_date": today.isoformat(),"temperature_unit": "fahrenheit",},)
    assert response.status_code == 404


def test_create_handles_weather_api_failure(monkeypatch,):
    async def fake_prepare_document(request_data,settings,):
        raise ExternalAPIError("The weather service could not be reached.")
    monkeypatch.setattr(records_route,"prepare_weather_record_document",fake_prepare_document,)
    today = date.today()
    response = client.post("/api/weather-records",json={"location": "Binghamton, NY","start_date": today.isoformat(),"end_date": today.isoformat(),"temperature_unit": "fahrenheit",},)
    assert response.status_code == 502


def test_create_handles_database_failure(monkeypatch,):
    app.state.weather_collection = FailingCollection()
    async def fake_prepare_document(request_data,settings,):
        return sample_weather_document()
    monkeypatch.setattr(records_route,"prepare_weather_record_document",fake_prepare_document,)
    today = date.today()
    response = client.post("/api/weather-records",json={"location": "Binghamton, NY","start_date": today.isoformat(),"end_date": today.isoformat(),"temperature_unit": "fahrenheit",},)
    assert response.status_code == 503
    assert response.json() == {
        "detail": ("The database is currently unavailable.")
    }