from datetime import date, datetime, timedelta, timezone
from bson import ObjectId
from fastapi.testclient import TestClient
from pymongo.errors import ConnectionFailure
from app.main import app

client = TestClient(app)

def create_weather_document(record_id: ObjectId | None = None,location: str = "Binghamton, NY",created_at: datetime | None = None,):
    today = date.today()
    timestamp = created_at or datetime.now(timezone.utc)
    return {
        "_id": record_id or ObjectId(),
        "location_query": location,
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
        "air_quality": None,
        "travel_insights": [],
        "created_at": timestamp,
        "updated_at": timestamp,
    }


class FakeCursor:
    def __init__(self, documents: list[dict]) -> None:
        self.documents = list(documents)

    def sort(self,field_name: str,direction: int,):
        self.documents.sort(key=lambda document: document[field_name],reverse=direction == -1,)
        return self

    def skip(self, number: int):
        self.documents = self.documents[number:]
        return self

    def limit(self, number: int):
        self.documents = self.documents[:number]
        return self

    async def to_list(self,length:int | None = None,):
        if length is None:
            return self.documents
        return self.documents[:length]

class SuccessfulReadCollection:
    def __init__(self,documents: list[dict],):
        self.documents = documents

    def find(self, query: dict):
        assert query == {}
        return FakeCursor(self.documents)

    async def find_one(self,query: dict,):
        requested_id = query.get("_id")
        for document in self.documents:
            if document["_id"] == requested_id:
                return document

        return None


class FailingReadCollection:
    def find(self, query: dict):
        raise ConnectionFailure("Test database failure")

    async def find_one(self, query: dict):raise ConnectionFailure("Test database failure")

def test_read_all_weather_records():
    older_time = datetime.now(timezone.utc) - timedelta(hours=1)
    newer_time = datetime.now(timezone.utc)
    older_document = create_weather_document(location="Older location",created_at=older_time,)

    newer_document = create_weather_document(location="Newer location",created_at=newer_time,)

    app.state.weather_collection = (SuccessfulReadCollection([older_document,newer_document,]))
    response = client.get("/api/weather-records",params={"skip": 0,"limit": 20,},)
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) == 2
    assert response_data[0]["location_query"] == ("Newer location")
    assert response_data[1]["location_query"] == ("Older location")
    assert "_id" not in response_data[0]
    assert len(response_data[0]["id"]) == 24

def test_read_one_weather_record():
    record_id = ObjectId()
    document = create_weather_document(record_id=record_id)
    app.state.weather_collection = (SuccessfulReadCollection([document]))
    response = client.get(f"/api/weather-records/{record_id}")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == str(record_id)
    assert response_data["location_query"] == ("Binghamton, NY")

def test_read_one_rejects_invalid_id():
    app.state.weather_collection = (SuccessfulReadCollection([]))
    response = client.get("/api/weather-records/abc")

    assert response.status_code == 400
    assert response.json() == {"detail": "'abc' is not a valid weather record ID."}

def test_read_one_returns_404():
    app.state.weather_collection = (SuccessfulReadCollection([]))
    missing_id = ObjectId()
    response = client.get(f"/api/weather-records/{missing_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": f"Weather record '{missing_id}' was not found."}

def test_read_handles_database_failure():
    app.state.weather_collection = (FailingReadCollection())
    response = client.get("/api/weather-records")
    assert response.status_code == 503
    assert response.json() == {"detail":"The database is currently unavailable."}