import csv
import io
import json
from datetime import datetime, timezone
from typing import Any
from fastapi.encoders import jsonable_encoder

CSV_COLUMNS = ["id","location_query","resolved_name","state","country","postal_code","latitude","longitude","start_date","end_date","weather_source","temperature_unit",
    "wind_speed_unit","precipitation_unit","current_temperature","current_condition","timezone","timezone_abbreviation","forecast_json","air_quality_json","travel_insights_json",
    "created_at","updated_at",]


async def read_export_documents(collection,) :
    cursor = collection.find({}).sort("created_at",-1,)
    return await cursor.to_list(None)

def normalize_document_for_export(document,):
    normalized_document = {**document,"id": str(document["_id"]),}
    normalized_document.pop("_id", None)
    return jsonable_encoder(normalized_document)


def build_json_export(documents,):
    normalized_documents = [normalize_document_for_export(document) for document in documents]
    return json.dumps(normalized_documents,indent=2,ensure_ascii=False,)

def build_csv_export(documents,):
    output = io.StringIO(newline="")
    writer = csv.DictWriter(output,fieldnames=CSV_COLUMNS,extrasaction="ignore",)
    writer.writeheader()
    for document in documents:
        normalized_document = normalize_document_for_export(document)
        resolved_location = normalized_document.get("resolved_location") or {}

        current_weather = normalized_document.get("current_weather") or {}
        forecast=normalized_document.get("forecast") or []
        air_quality=normalized_document.get("air_quality")
        travel_insights = normalized_document.get("travel_insights") or []
        writer.writerow({"id": normalized_document.get("id"),
                "location_query": normalized_document.get("location_query"),
                "resolved_name": resolved_location.get("name"),
                "state": resolved_location.get("state"),
                "country": resolved_location.get("country"),
                "postal_code": resolved_location.get("postal_code"),
                "latitude": resolved_location.get("latitude"),
                "longitude": resolved_location.get("longitude"),
                "start_date": normalized_document.get("start_date"),
                "end_date": normalized_document.get("end_date"),
                "weather_source": normalized_document.get("weather_source"),
                "temperature_unit":normalized_document.get("temperature_unit"),
                "wind_speed_unit":normalized_document.get("wind_speed_unit"),
                "precipitation_unit": normalized_document.get("precipitation_unit"),
                "current_temperature":current_weather.get("temperature"),
                "current_condition":current_weather.get("condition"),
                "timezone": normalized_document.get("timezone"),
                "timezone_abbreviation": normalized_document.get("timezone_abbreviation"),
                "forecast_json": json.dumps(forecast,ensure_ascii=False,),
                "air_quality_json": json.dumps(air_quality,ensure_ascii=False,),
                "travel_insights_json":json.dumps(travel_insights,ensure_ascii=False,),
                "created_at": normalized_document.get("created_at"),
                "updated_at":normalized_document.get("updated_at"),
                })

    return "\ufeff" + output.getvalue()

def create_export_filename(export_format,):
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    return (f"weather-records-{timestamp}.{export_format}")