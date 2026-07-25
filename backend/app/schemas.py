from datetime import date, datetime
from typing import Literal, Self
from pydantic import BaseModel, Field,ConfigDict,model_validator

TemperatureUnit = Literal["celsius","fahrenheit"]

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
        values= [self.location,self.latitude,self.longitude,self.start_date,self.end_date,self.temperature_unit,]
        if all(value is None for value in values):
            raise ValueError("Provide at least one field to update.")
        has_location= bool(self.location)
        has_latitude= self.latitude is not None
        has_longitude= self.longitude is not None
        if has_latitude!= has_longitude:
            raise ValueError("Latitude and longitude must be provided together.")
        if has_location and (has_latitude or has_longitude):
            raise ValueError("Provide either a location or GPS coordinates, not both.")
        if (self.start_date is not None and self.end_date is not None):
            if self.end_date < self.start_date:
                raise ValueError("End date must be the same as or later than start date.")
            number_of_days = (self.end_date - self.start_date).days + 1
            if number_of_days > 5:
                raise ValueError( "The selected date range cannot exceed five days.")
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

class ForecastDay(BaseModel):
    forecast_date:date
    minimum_temperature:float
    maximum_temperature:float
    precipitation_probability:float | None = Field(default=None,ge=0,le=100,)
    maximum_wind_speed:float | None = Field(default=None,ge=0,)
    weather_code:int | None = None
    condition:str

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
    temperature_unit:TemperatureUnit
    current_weather:CurrentWeather
    forecast:list[ForecastDay]

    air_quality:AirQuality | None = None
    travel_insights:list[str] = Field(default_factory=list,)

    created_at:datetime
    updated_at:datetime
    model_config= ConfigDict(extra="ignore",)


class ErrorResponse(BaseModel):
    detail:str