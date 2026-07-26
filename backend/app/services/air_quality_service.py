from datetime import datetime
from typing import Any
import httpx
from app.config import Settings
from app.exceptions import ExternalAPIError
from app.schemas import AirQualityResponse


def optional_float(value):
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None

def get_aqi_category(us_aqi,):
    if us_aqi is None:
        return "Unavailable"
    if us_aqi<=50:
        return "Good"
    if us_aqi<=100:
        return "Moderate"
    if us_aqi<=150:
        return "Unhealthy for sensitive groups"
    if us_aqi<=200:
        return "Unhealthy"
    if us_aqi<=300:
        return "Very unhealthy"
    return "Hazardous"

def parse_air_quality_response(response_data,):
    current_data = response_data.get("current")
    if not isinstance(current_data, dict):
        raise ExternalAPIError("The air-quality service has no current data.")
    observed_at= None
    observed_at_value = current_data.get("time")
    if observed_at_value:
        try:
            observed_at = datetime.fromisoformat(str(observed_at_value))
        except ValueError:
            observed_at = None
    us_aqi = optional_float(current_data.get("us_aqi"))
    return AirQualityResponse(observed_at=observed_at,us_aqi=us_aqi,category=get_aqi_category(us_aqi),pm2_5=optional_float(current_data.get("pm2_5")),pm10=optional_float(current_data.get("pm10")),uv_index=optional_float(current_data.get("uv_index")),)

async def fetch_air_quality(latitude,longitude,settings,):
    parameters = {"latitude": latitude,"longitude": longitude,"current": ",".join(["us_aqi","pm2_5","pm10","uv_index",]),"timezone": "auto",}
    try:
        async with httpx.AsyncClient(timeout=(settings.external_api_timeout_seconds),) as client:
            response = await client.get(settings.air_quality_api_url,params=parameters,)
            response.raise_for_status()
    except httpx.TimeoutException as error:
        raise ExternalAPIError("The air-quality service timed out.") from error
    except httpx.HTTPStatusError as error:
        reason:str | None = None
        try:
            error_data= error.response.json()
            if isinstance(error_data, dict):
                reason= error_data.get("reason")
        except ValueError:
            reason= None
        raise ExternalAPIError(reason or "The air-quality service rejected the request.") from error
    except httpx.RequestError as error:
        raise ExternalAPIError("The air-quality service could not be reached.") from error
    try:
        response_data = response.json()
    except ValueError as error:
        raise ExternalAPIError("The air-quality service returned invalid JSON.") from error
    if not isinstance(response_data, dict):
        raise ExternalAPIError("The air-quality service returned an unexpected response.")
    return parse_air_quality_response(response_data)