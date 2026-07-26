import csv
import io
from datetime import date, datetime, timezone
from bson import ObjectId
from fastapi.testclient import TestClient
from pymongo.errors import ConnectionFailure
from app.main import app

client = TestClient(app)

def create_export_document() :
    today = date.today()
    timestamp = datetime.now(timezone.utc)
    return {"_id": ObjectId(),"location_query": "Binghamton, NY",
        "resolved_location": {"name": "Binghamton","state": "New York","country": "United States","postal_code": "13901","latitude": 42.0987,"longitude": -75.9180,},
        "start_date": today.isoformat(),"end_date": today.isoformat(),"weather_source": "forecast","temperature_unit": "fahrenheit","wind_speed_unit": "mph","precipitation_unit": "inch",
        "timezone": "America/New_York","timezone_abbreviation": "EDT",
        "current_weather": {"temperature": 78.0,"condition": "Partly cloudy",},
        "forecast":[{"forecast_date": (today.isoformat()),"minimum_temperature": 64.0,"maximum_temperature": 82.0,"condition": "Partly cloudy",}],
        "air_quality": None,
        "travel_insights": ["Good conditions for outdoor activities."],
        "created_at": timestamp,
        "updated_at": timestamp,
    }

class FakeExportCursor:
    def __init__(self,documents,):
        self.documents = list(documents)

    def sort(self,field_name,direction,):
        self.documents.sort(key=lambda document: document[field_name],reverse=direction == -1,)
        return self

    async def to_list(self,length=None,):
        if length is None:
            return self.documents
        return self.documents[:length]


class SuccessfulExportCollection:
    def __init__(self,documents,):
        self.documents = documents

    def find(self, query,):
        assert query == {}
        return FakeExportCursor(self.documents)

class FailingExportCollection:
    def find(self, query):
        raise ConnectionFailure("Test database failure")

def test_export_records_as_json():
    document = create_export_document()
    app.state.weather_collection = (SuccessfulExportCollection([document]))

    response = client.get("/api/weather-records/export/json")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")
    assert "attachment;" in response.headers["content-disposition"]
    assert ".json" in response.headers["content-disposition"]
    response_data = response.json()
    assert len(response_data) == 1
    assert response_data[0]["id"] == str(document["_id"])
    assert "_id" not in response_data[0]
    assert response_data[0]["location_query"] == "Binghamton, NY"


def test_export_records_as_csv():
    document = create_export_document()
    app.state.weather_collection = (
        SuccessfulExportCollection([document]))

    response = client.get("/api/weather-records/export/csv")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/csv")
    assert ".csv" in response.headers["content-disposition"]
    decoded_content = response.content.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(decoded_content))
    rows = list(reader)
    assert len(rows) == 1
    assert rows[0]["id"] == str(document["_id"])
    assert rows[0]["location_query"] == "Binghamton, NY"
    assert rows[0]["resolved_name"] =="Binghamton"
    assert rows[0]["current_temperature"] == "78.0"

def test_export_empty_collection_as_json():
    app.state.weather_collection = SuccessfulExportCollection([])
    response = client.get("/api/weather-records/export/json")
    assert response.status_code == 200
    assert response.json() == []

def test_export_rejects_unsupported_format():
    app.state.weather_collection=SuccessfulExportCollection([])
    response = client.get("/api/weather-records/export/pdf")
    assert response.status_code == 422

def test_export_handles_database_failure():
    app.state.weather_collection = (FailingExportCollection())
    response = client.get("/api/weather-records/export/json")
    assert response.status_code == 503
    assert response.json() == {"detail": ("The database is currently unavailable.")}