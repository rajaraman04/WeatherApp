from datetime import date, datetime, timezone
from types import SimpleNamespace
from bson import ObjectId
from fastapi.testclient import TestClient
from pymongo.errors import ConnectionFailure
from app.main import app
from app.routes import weather_records as records_route
from app.schemas import WeatherRecordResponse
from app.schemas import WeatherRecordUpdate
from app.services.weather_record_service import build_complete_update_request

client = TestClient(app)

def sample_updated_response(record_id,):
    today = date.today()
    timestamp = datetime.now(timezone.utc)
    return WeatherRecordResponse(
        id=str(record_id),
        location_query="Boston, MA",
        resolved_location={"name": "Boston","state": "Massachusetts","country": "United States","postal_code": "02108","latitude": 42.3601,"longitude": -71.0589,},
        start_date=today,end_date=today,weather_source="forecast",temperature_unit="celsius",wind_speed_unit="kmh",precipitation_unit="mm",timezone="America/New_York",timezone_abbreviation="EDT",
        current_weather={"temperature": 25.0,"condition": "Partly cloudy",},
        forecast=[{"forecast_date": today,"minimum_temperature": 18.0,"maximum_temperature": 27.0,"condition": "Partly cloudy",}],
        air_quality=None,travel_insights=[],created_at=timestamp,updated_at=timestamp,)


def test_update_weather_record(monkeypatch,):
    record_id = ObjectId()
    async def fake_update_record(collection,record_id,update_data,settings,):
        assert update_data.location == "Boston, MA"
        return sample_updated_response(ObjectId(record_id))
    monkeypatch.setattr(records_route,"update_weather_record_by_id",fake_update_record,)
    app.state.weather_collection = SimpleNamespace()
    response = client.patch(f"/api/weather-records/{record_id}",json={"location": "Boston, MA","temperature_unit": "celsius",},)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == str(record_id)
    assert response_data["location_query"] == ("Boston, MA")
    assert response_data["temperature_unit"] == ("celsius")

def test_update_rejects_empty_body():
    record_id = ObjectId()
    response = client.patch(f"/api/weather-records/{record_id}",json={},)
    assert response.status_code == 422

def test_update_rejects_partial_coordinates():
    record_id = ObjectId()
    response = client.patch(f"/api/weather-records/{record_id}",json={"latitude": 40.7128,},)
    assert response.status_code == 422

def test_update_rejects_location_and_coordinates():
    record_id = ObjectId()
    response = client.patch(f"/api/weather-records/{record_id}",json={"location": "New York","latitude": 40.7128,"longitude": -74.006,},)
    assert response.status_code == 422

def test_update_handles_database_failure(monkeypatch,):
    record_id = ObjectId()
    async def fake_update_record(collection,record_id,update_data,settings,):
        raise ConnectionFailure("Test database failure")
    monkeypatch.setattr(records_route,"update_weather_record_by_id",fake_update_record,)
    app.state.weather_collection = SimpleNamespace()
    response = client.patch(f"/api/weather-records/{record_id}",json={"temperature_unit": "celsius",},)
    assert response.status_code == 503
    assert response.json() == {"detail": ("The database is currently unavailable.")}
def test_build_complete_update_request():
    today = date.today()
    existing_document = {"location_query": "Binghamton, NY",
        "resolved_location": {"name": "Binghamton","state": "New York","country": "United States","latitude": 42.0987,"longitude": -75.918,},
        "start_date": today.isoformat(),"end_date": today.isoformat(),"temperature_unit": "fahrenheit",}
    update_data = WeatherRecordUpdate(temperature_unit="celsius")

    complete_request = build_complete_update_request(existing_document=existing_document,update_data=update_data,)
    assert complete_request.location == ("Binghamton, NY")
    assert complete_request.start_date == today
    assert complete_request.end_date == today
    assert complete_request.temperature_unit == ("celsius")