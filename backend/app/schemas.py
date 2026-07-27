from datetime import date, datetime, timedelta
from typing import Literal, Self
from pydantic import BaseModel, Field,ConfigDict,model_validator
from zoneinfo import ZoneInfo
from app.config import get_settings

TemperatureUnit = Literal["celsius","fahrenheit"]
WindSpeedUnit = Literal["kmh", "mph"]
PrecipitationUnit = Literal["mm", "inch"]
WeatherSource = Literal["forecast", "historical"]
ExportFormat = Literal["json", "csv"]

def get_application_today():
    settings = get_settings()
    return datetime.now(ZoneInfo(settings.app_timezone)).date()

class WeatherRecordCreate(BaseModel):
    location:str | None = Field(default=None,min_length=2,max_length=120,examples=["Binghamton, NY"],)
    latitude:float | None = Field(default=None,ge=-90,le=90,examples=[42.0987],)
    longitude:float | None = Field(default=None,ge=-180,le=180,examples=[-75.9180],)
    start_date:date
    end_date:date
    temperature_unit: TemperatureUnit = "Fahrenheit"
    model_config= ConfigDict( str_strip_whitespace=True,extra="forbid",)

    @model_validator(mode="after")
    def validate_location_source(self):
        has_location= bool(self.location)
        has_latitude= self.latitude is not None
        has_longitude= self.longitude is not None

        if has_location and (has_latitude or has_longitude):
            raise ValueError("Provide either a location or GPS coordinates, not both.")
        if not has_location and not (has_latitude and has_longitude):
            raise ValueError("Provide a location or both latitude and longitude.")
        return self

    @model_validator(mode="after")
    def validate_date_range(self):
        if self.end_date < self.start_date:
            raise ValueError("End date must be the same as or later than start date.")
        number_of_days = (self.end_date - self.start_date).days + 1
        if number_of_days > 5:
            raise ValueError("The selected date range cannot exceed five days.")
        today = get_application_today()
        if self.start_date < today:
            raise ValueError("Start date cannot be in the past.")
        latest_supported_date = today + timedelta(days=15)
        if self.end_date > latest_supported_date:
            raise ValueError("End date cannot be more than 15 days from today.")
        return self

class WeatherRecordUpdate(BaseModel):
    location:str | None = Field(default=None,min_length=2,max_length=120,)
    latitude:float | None = Field(default=None,ge=-90,le=90,)
    longitude:float | None = Field(default=None,ge=-180,le=180,)
    start_date:date | None = None
    end_date:date | None = None
    temperature_unit:TemperatureUnit | None = None
    model_config= ConfigDict(str_strip_whitespace=True,extra="forbid",)

    @model_validator(mode="after")
    def validate_update_values(self):
        supplied_values = self.model_dump(exclude_unset=True)
        if not supplied_values:
            raise ValueError("Provide at least one field to update.")
        has_location= ("location" in supplied_values and self.location is not None)
        has_latitude= self.latitude is not None
        has_longitude= self.longitude is not None
        if has_latitude!= has_longitude:
            raise ValueError("Latitude and longitude must be provided together.")
        if has_location and (has_latitude or has_longitude):
            raise ValueError("Provide either a location or GPS coordinates, not both.")
        if (self.start_date is not None and self.end_date is not None):
            if self.end_date < self.start_date:
                raise ValueError("End date must be the same as or later than start date.")
            selected_days = (self.end_date - self.start_date).days + 1
            if selected_days > 5:
                raise ValueError("The selected date range cannot exceed five days.")
        return self
    
class LocationSearchResult(BaseModel):
    name:str
    state:str | None = None
    country:str
    country_code:str
    postal_code:str | None = None
    latitude:float
    longitude:float
    timezone:str | None = None

class ResolvedLocation(BaseModel):
    name:str
    state:str | None = None
    country:str
    postal_code:str | None = None
    latitude:float
    longitude:float

class CurrentWeather(BaseModel):
    temperature:float
    feels_like:float | None = None
    humidity:float | None = Field(default=None,ge=0,le=100,)
    wind_speed:float | None = Field(default=None,ge=0,)
    precipitation:float | None = Field(default=None,ge=0,)
    weather_code:int | None = None
    condition:str
    observed_at:datetime | None = None
    is_day: bool | None = None

class ForecastDay(BaseModel):
    forecast_date:date
    minimum_temperature:float
    maximum_temperature:float
    precipitation_probability:float | None=Field(default=None,ge=0,le=100,)
    precipitation_sum:float | None=Field(default=None,ge=0,)

    maximum_wind_speed:float | None=Field(default=None,ge=0,)
    weather_code:int | None=None
    condition:str
    sunrise:datetime | None=None
    sunset:datetime | None=None

class AirQuality(BaseModel):
    us_aqi:float | None = Field(default=None,ge=0,)
    pm2_5:float | None = Field(default=None,ge=0,)
    pm10:float | None = Field(default=None,ge=0,)
    uv_index:float | None = Field(default=None,ge=0,)

class WeatherRecordResponse(BaseModel):
    id:str
    location_query:str | None = None
    resolved_location:ResolvedLocation
    start_date:date
    end_date:date
    weather_source: WeatherSource
    temperature_unit:TemperatureUnit
    wind_speed_unit:WindSpeedUnit
    precipitation_unit:PrecipitationUnit
    timezone:str
    timezone_abbreviation:str | None = None
    current_weather:CurrentWeather
    forecast:list[ForecastDay]
    air_quality:AirQuality | None = None
    travel_insights:list[str] = Field(default_factory=list,)
    created_at:datetime
    updated_at:datetime
    model_config= ConfigDict(extra="ignore",)

class WeatherQuery(BaseModel):
    latitude:float=Field(ge=-90,le=90,examples=[42.0987],)
    longitude:float=Field(ge=-180,le=180,examples=[-75.9180],)
    start_date:date
    end_date:date
    temperature_unit:TemperatureUnit="fahrenheit"
    model_config=ConfigDict(extra="forbid",)

    @model_validator(mode="after")
    def validate_forecast_dates(self):
        if self.end_date < self.start_date:
            raise ValueError("End date must be the same as or later than start date.")
        selected_days=(self.end_date-self.start_date).days + 1
        if selected_days > 5:
            raise ValueError("The selected date range cannot exceed 5 days.")
        today = get_application_today()
        if self.start_date < today:
            raise ValueError("Start date cannot be in past.")
        latest_supported_date = today + timedelta(days=15)
        if self.end_date > latest_supported_date:
            raise ValueError("End date cannot be more than 15 days from today.")
        return self

class WeatherDataResponse(BaseModel):
    latitude:float
    longitude:float
    timezone:str
    timezone_abbreviation:str | None = None
    temperature_unit:TemperatureUnit
    wind_speed_unit:WindSpeedUnit
    precipitation_unit:PrecipitationUnit
    current_weather:CurrentWeather
    forecast:list[ForecastDay]

class AirQualityResponse(BaseModel):
    observed_at:datetime | None= None
    us_aqi:float | None= None
    category:str
    pm2_5:float | None= None
    pm10:float | None= None
    uv_index:float | None= None

class ErrorResponse(BaseModel):
    detail:str