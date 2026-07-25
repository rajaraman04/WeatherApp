from datetime import date, datetime, timezone
from typing import Any
from app.config import Settings
from app.schemas import ResolvedLocation,WeatherQuery,WeatherRecordCreate
from app.services.geocoding_service import search_locations
from app.services.weather_service import fetch_weather
from bson import ObjectId
from app.exceptions import InvalidWeatherRecordIdError,WeatherRecordNotFoundError
from app.schemas import ResolvedLocation,WeatherQuery,WeatherRecordCreate,WeatherRecordResponse,WeatherRecordUpdate

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

def serialize_weather_record(document,) :
    response_data = {**document,"id": str(document["_id"]),}
    response_data.pop("_id", None)
    return WeatherRecordResponse.model_validate(response_data)

async def read_weather_records(collection,skip,limit,):
    cursor = (collection.find({}).sort("created_at", -1).skip(skip).limit(limit))
    documents = await cursor.to_list(length=limit)
    return [serialize_weather_record(document) for document in documents]

async def read_weather_record_by_id(collection,record_id,):
    if not ObjectId.is_valid(record_id):
        raise InvalidWeatherRecordIdError(record_id)
    document = await collection.find_one({"_id": ObjectId(record_id),})
    if document is None:
        raise WeatherRecordNotFoundError(record_id)
    return serialize_weather_record(document)

def build_complete_update_request(existing_document,update_data,):
    provided_fields = update_data.model_dump(exclude_unset=True)
    existing_location_query = existing_document.get("location_query")
    existing_resolved_location = existing_document["resolved_location"]

    location:str | None= None
    latitude:float | None= None
    longitude:float | None= None
    location_was_updated =("location" in provided_fields and update_data.location is not None)
    coordinates_were_updated = (update_data.latitude is not None and update_data.longitude is not None)

    if location_was_updated:
        location = update_data.location
    elif coordinates_were_updated:
        latitude = update_data.latitude
        longitude = update_data.longitude
    elif existing_location_query:
        location = existing_location_query
    else:
        latitude = float(existing_resolved_location["latitude"])
        longitude = float(existing_resolved_location["longitude"])

    existing_start_date = date.fromisoformat(str(existing_document["start_date"]))
    existing_end_date = date.fromisoformat(str(existing_document["end_date"]))
    final_start_date = (update_data.start_date if update_data.start_date is not None else existing_start_date)
    final_end_date = (update_data.end_date if update_data.end_date is not None else existing_end_date)
    final_temperature_unit = (update_data.temperature_unit if update_data.temperature_unit is not None else existing_document["temperature_unit"])
    return WeatherRecordCreate(location=location,latitude=latitude,longitude=longitude,start_date=final_start_date,end_date=final_end_date,temperature_unit=final_temperature_unit,)

async def update_weather_record_by_id(collection,record_id,update_data,settings,):
    if not ObjectId.is_valid(record_id):
        raise InvalidWeatherRecordIdError(record_id)
    object_id = ObjectId(record_id)
    existing_document = await collection.find_one({"_id": object_id,})

    if existing_document is None:
        raise WeatherRecordNotFoundError(record_id)

    complete_request = build_complete_update_request(existing_document=existing_document,update_data=update_data,)
    refreshed_document = (await prepare_weather_record_document(request_data=complete_request,settings=settings,))
    refreshed_document.pop("created_at", None)
    await collection.update_one({"_id": object_id,},{"$set": refreshed_document,},)
    updated_document = await collection.find_one({"_id": object_id,})
    if updated_document is None:
        raise WeatherRecordNotFoundError(record_id)
    return serialize_weather_record(updated_document)

async def delete_weather_record_by_id(collection,record_id,):
    if not ObjectId.is_valid(record_id):
        raise InvalidWeatherRecordIdError(record_id)
    delete_result = await collection.delete_one({"_id": ObjectId(record_id),})
    if delete_result.deleted_count == 0:
        raise WeatherRecordNotFoundError(record_id)