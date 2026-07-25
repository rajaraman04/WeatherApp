from fastapi.testclient import TestClient
from pymongo.errors import ConnectionFailure

from app.main import app
client = TestClient(app)

class SuccessfulAdmin:
    async def command(self, command: dict) -> dict:
        assert command == {"ping": 1}
        return {"ok": 1}

class SuccessfulMongoClient:
    def __init__(self):
        self.admin = SuccessfulAdmin()

class FailingAdmin:
    async def command(self, command: dict):
        raise ConnectionFailure("Test database connection failure")

class FailingMongoClient:
    def __init__(self):
        self.admin = FailingAdmin()

def test_root_endpoint() :
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Weather App API!","documentation": "/docs",}

def test_health_endpoint_when_database_is_connected():
    app.state.mongodb_client = SuccessfulMongoClient()
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy","service": "Weather App API","version": "1.0.0","database": "connected",}


def test_health_endpoint_when_database_is_unavailable():
    app.state.mongodb_client = FailingMongoClient()
    response = client.get("/api/health")
    assert response.status_code == 503
    assert response.json() == {"detail": "MongoDB is currently unavailable."}