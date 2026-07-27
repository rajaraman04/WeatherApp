from datetime import date,timedelta
import pytest
from pydantic import ValidationError
from app.schemas import WeatherRecordCreate,WeatherRecordUpdate,get_application_today

def test_create_schema_accepts_location():
    today = get_application_today()
    end_date = today + timedelta(days=4)
    record = WeatherRecordCreate(location="Binghamton, NY",start_date=today,end_date=end_date,temperature_unit="fahrenheit",)
    assert record.location == "Binghamton, NY"
    assert record.start_date == today
    assert record.end_date == end_date
    assert record.temperature_unit == "fahrenheit"

def test_create_schema_accepts_coordinates():
    today=get_application_today()
    end_date=today + timedelta(days=4)
    record=WeatherRecordCreate(latitude=42.0987,longitude=-75.9180,start_date=today,end_date=end_date,)
    assert record.latitude==42.0987
    assert record.longitude==-75.9180
    assert record.start_date==today
    assert record.end_date==end_date

def test_create_schema_rejects_missing_location():
    with pytest.raises(ValidationError,match="Provide a location or both latitude and longitude",):
        WeatherRecordCreate(start_date=date(2026, 7, 25),end_date=date(2026, 7, 29),)

def test_create_schema_rejects_partial_coordinates():
    with pytest.raises(ValidationError,match="Provide a location or both latitude and longitude",):
        WeatherRecordCreate(latitude=42.0987,start_date=date(2026, 7, 25),end_date=date(2026, 7, 29),)

def test_create_schema_rejects_reversed_dates():
    with pytest.raises(ValidationError,match="End date must be the same as or later",):
        WeatherRecordCreate(location="Binghamton, NY",start_date=date(2026, 7, 29),end_date=date(2026, 7, 25),)

def test_create_schema_rejects_more_than_five_days():
    with pytest.raises(ValidationError,match="cannot exceed five days",):
        WeatherRecordCreate(location="Binghamton, NY",start_date=date(2026, 7, 25),end_date=date(2026, 7, 30),)

def test_update_schema_rejects_empty_request():
    with pytest.raises(ValidationError,match="Provide at least one field to update",):
        WeatherRecordUpdate()