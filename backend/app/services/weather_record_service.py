from datetime import datetime, timezone
from typing import Any
from app.config import Settings
from app.schemas import ResolvedLocation,WeatherQuery,WeatherRecordCreate
from app.services.geocoding_service import search_locations
from app.services.weather_service import fetch_weather


async def resolve_requested_location(request_data,settings,):
    if request_data.location is not None:
        matching_locations = await search_locations(query=request_data.location,limit=1,settings=settings,)
        selected_location = matching_locations[0]
        return ResolvedLocation(name=selected_location.name,state=selected_location.state,country=selected_location.country,postal_code=selected_location.postal_code,latitude=selected_location.latitude,longitude=selected_location.longitude,)
    if(request_data.latitude is None or request_data.longitude is None):
        raise ValueError("Latitude and longitude are required.")
    return ResolvedLocation(name="Current location",state=None,country="Unknown",postal_code=None,latitude=request_data.latitude,longitude=request_data.longitude,)

async def prepare_weather_record_document(request_data,settings,):
    resolved_location = await resolve_requested_location(request_data=request_data,settings=settings,)
    weather_query = WeatherQuery(latitude=resolved_location.latitude,longitude=resolved_location.longitude,start_date=request_data.start_date,end_date=request_data.end_date,temperature_unit=request_data.temperature_unit,)
    weather_data = await fetch_weather(query=weather_query,settings=settings,)
    current_time = datetime.now(timezone.utc)

    return {
        "location_query": request_data.location,
        "resolved_location": resolved_location.model_dump(mode="json"),
        "start_date": request_data.start_date.isoformat(),
        "end_date": request_data.end_date.isoformat(),
        "weather_source": "forecast",
        "temperature_unit": weather_data.temperature_unit,
        "wind_speed_unit": weather_data.wind_speed_unit,
        "precipitation_unit":weather_data.precipitation_unit,
        "timezone": weather_data.timezone,
        "timezone_abbreviation":weather_data.timezone_abbreviation,
        "current_weather":weather_data.current_weather.model_dump(mode="json"),
        "forecast":[forecast_day.model_dump(mode="json") for forecast_day in weather_data.forecast],
        "air_quality":None,
        "travel_insights":[],
        "created_at":current_time,
        "updated_at":current_time,
    }