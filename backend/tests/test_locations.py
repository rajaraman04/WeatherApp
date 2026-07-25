import pytest
from fastapi.testclient import TestClient
from app.config import Settings, get_settings
from app.exceptions import ExternalAPIError,LocationNotFoundError
from app.main import app
from app.routes import locations as locations_route
from app.schemas import LocationSearchResult

client = TestClient(app)

@pytest.fixture(autouse=True)
def override_settings():
    test_settings = Settings(mongodb_uri="mongodb://test",)
    app.dependency_overrides[get_settings] = (lambda: test_settings)
    yield
    app.dependency_overrides.clear()

def test_search_location_returns_results(monkeypatch,):
    async def fake_search_locations(query,limit,settings,):
        assert query == "Binghamton"
        assert limit == 5
        return [LocationSearchResult(name="Binghamton",state="New York",country="United States",country_code="US",postal_code="13901",latitude=42.0987,longitude=-75.9180,timezone="America/New_York",)]
    monkeypatch.setattr(locations_route,"search_locations",fake_search_locations,)
    response= client.get("/api/locations/search",params={"q": "Binghamton","limit": 5,},)
    assert response.status_code== 200
    response_data = response.json()
    assert len(response_data)== 1
    assert response_data[0]["name"]== "Binghamton"
    assert response_data[0]["country_code"]== "US"
    assert response_data[0]["latitude"]== 42.0987

def test_search_location_returns_404(monkeypatch,):
    async def fake_search_locations(query,limit,settings,):
        raise LocationNotFoundError(query)
    monkeypatch.setattr(locations_route,"search_locations",fake_search_locations,)
    response = client.get("/api/locations/search",params={"q": "UnknownPlace"},)
    assert response.status_code == 404
    assert response.json() == {"detail": ("No matching location was found for 'UnknownPlace'.")}

def test_search_location_handles_api_failure(monkeypatch,):
    async def fake_search_locations(query,limit,settings,):
        raise ExternalAPIError("The location service could not be reached.")
    monkeypatch.setattr(locations_route,"search_locations",fake_search_locations,)
    response = client.get("/api/locations/search",params={"q": "Binghamton"},)
    assert response.status_code == 502
    assert response.json() == {"detail": ("The location service could not be reached.")}

def test_search_location_rejects_short_query():
    response = client.get("/api/locations/search",params={"q": "B"},)
    assert response.status_code == 422

def test_search_location_rejects_large_limit():
    response = client.get("/api/locations/search",params={"q": "Binghamton","limit": 20,},)
    assert response.status_code == 422