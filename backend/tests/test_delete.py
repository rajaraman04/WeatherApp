from types import SimpleNamespace
from bson import ObjectId
from fastapi.testclient import TestClient
from pymongo.errors import ConnectionFailure
from app.main import app

client = TestClient(app)

class SuccessfulDeleteCollection:
    def __init__(self):
        self.deleted_query:dict|None = None
    async def delete_one(self,query,):
        self.deleted_query=query
        return SimpleNamespace(deleted_count=1)

class MissingDeleteCollection:
    async def delete_one(self,query,):
        return SimpleNamespace(deleted_count=0)

class FailingDeleteCollection:
    async def delete_one(self,query,):
        raise ConnectionFailure("Test database failure")

def test_delete_weather_record():
    record_id= ObjectId()
    fake_collection= SuccessfulDeleteCollection()
    app.state.weather_collection= fake_collection
    response = client.delete(f"/api/weather-records/{record_id}")
    assert response.status_code == 204
    assert response.content == b""
    assert fake_collection.deleted_query == {"_id": record_id}

def test_delete_rejects_invalid_id():
    app.state.weather_collection = (SuccessfulDeleteCollection())
    response = client.delete("/api/weather-records/abc")
    assert response.status_code == 400
    assert response.json() == {"detail": ("'abc' is not a valid weather record ID.")}

def test_delete_returns_404_when_missing():
    app.state.weather_collection = MissingDeleteCollection()
    record_id = ObjectId()
    response = client.delete(f"/api/weather-records/{record_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": f"Weather record '{record_id}' was not found."}

def test_delete_handles_database_failure():
    app.state.weather_collection=FailingDeleteCollection()
    record_id=ObjectId()
    response=client.delete(f"/api/weather-records/{record_id}")
    assert response.status_code==503
    assert response.json()=={"detail":"The database is currently unavailable."}