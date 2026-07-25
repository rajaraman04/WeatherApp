from fastapi.testclient import TestClient

from app.main import app
client = TestClient(app)

def test_root_endpoint():
    response=client.get("/")
    assert response.status_code == 200
    assert response.json()=={
        "message": "Welcome to the Weather App API!",
        "documentation": "/docs",
    }

def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "service": "Weather App API",
        "version": "1.0.0",
    }