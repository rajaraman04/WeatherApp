from datetime import datetime
import pytest
from app.services.air_quality_service import get_aqi_category,parse_air_quality_response


@pytest.mark.parametrize(("aqi", "expected_category"),[(None, "Unavailable"),(25, "Good"),(75, "Moderate"),(125,"Unhealthy for sensitive groups",),(175, "Unhealthy"),(250, "Very unhealthy"),(350, "Hazardous"),],)
def test_get_aqi_category(aqi,expected_category,):
    assert get_aqi_category(aqi)==expected_category

def test_parse_air_quality_response():
    response_data = {"current": {"time": "2026-07-26T15:00","us_aqi": 42,"pm2_5": 8.4,"pm10": 14.7,"uv_index": 6.2,}}
    result = parse_air_quality_response(response_data)
    assert result.observed_at == datetime(2026,7,26,15,0,)
    assert result.us_aqi==42
    assert result.category=="Good"
    assert result.pm2_5==8.4
    assert result.pm10==14.7
    assert result.uv_index==6.2