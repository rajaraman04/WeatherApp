from datetime import date, datetime
from typing import Any
import httpx
from app.config import Settings
from app.exceptions import ExternalAPIError
from app.schemas import CurrentWeather,ForecastDay,WeatherDataResponse,WeatherQuery


WEATHER_CODE_DESCRIPTIONS: dict[int, str] = {0: "Clear sky",1: "Mainly clear",2: "Partly cloudy",3: "Overcast",45: "Fog",48: "Depositing rime fog",51: "Light drizzle",
    53: "Moderate drizzle",55: "Dense drizzle",56: "Light freezing drizzle",57: "Dense freezing drizzle",61: "Slight rain",63: "Moderate rain",65: "Heavy rain",
    66: "Light freezing rain",67: "Heavy freezing rain",71: "Slight snowfall",73: "Moderate snowfall",75: "Heavy snowfall",77: "Snow grains",80: "Slight rain showers",
    81: "Moderate rain showers",82: "Violent rain showers", 85: "Slight snow showers",86: "Heavy snow showers",95: "Thunderstorm",96: "Thunderstorm with slight hail",99: "Thunderstorm with heavy hail",}


def weather_code_to_condition(weather_code,):
    if weather_code is None:
        return "Unknown"
    return WEATHER_CODE_DESCRIPTIONS.get(weather_code,"Unknown",)

def optional_float(value):
    if value is None:
        return None
    return float(value)

def parse_weather_response(response_data,query,):
    current_data=response_data.get("current")
    daily_data=response_data.get("daily")

    if not isinstance(current_data, dict):
        raise ExternalAPIError("The weather service returned no current weather data.")

    if not isinstance(daily_data, dict):
        raise ExternalAPIError("The weather service returned no forecast data.")

    try:
        current_weather_code = int(current_data["weather_code"])

        current_weather = CurrentWeather(temperature=float(current_data["temperature_2m"]),
            feels_like=optional_float(current_data.get("apparent_temperature")),
            humidity=optional_float(current_data.get("relative_humidity_2m")),
            wind_speed=optional_float(current_data.get("wind_speed_10m")),
            precipitation=optional_float(current_data.get("precipitation")),
            weather_code=current_weather_code,
            condition=weather_code_to_condition(current_weather_code),
            observed_at=datetime.fromisoformat(str(current_data["time"])),
            is_day=(None if current_data.get("is_day") is None else bool(current_data["is_day"])),)

    except (KeyError, TypeError, ValueError) as error:
        raise ExternalAPIError("The weather service returned incomplete current weather data.") from error

    required_daily_fields=["time","weather_code","temperature_2m_max","temperature_2m_min","precipitation_probability_max","precipitation_sum","wind_speed_10m_max","sunrise","sunset",]

    for field_name in required_daily_fields:
        if not isinstance(daily_data.get(field_name), list):
            raise ExternalAPIError(f"The weather forecast is missing '{field_name}'.")

    forecast_length=len(daily_data["time"])
    if forecast_length==0:
        raise ExternalAPIError("The weather service returned an empty forecast.")

    if any(len(daily_data[field_name]) != forecast_length for field_name in required_daily_fields):
        raise ExternalAPIError("The weather service returned inconsistent forecast data.")
    forecast:list[ForecastDay]=[]
    try:
        for index in range(forecast_length):
            weather_code = int(daily_data["weather_code"][index])
            forecast.append(ForecastDay(forecast_date=date.fromisoformat(str(daily_data["time"][index])),
                    minimum_temperature=float(daily_data["temperature_2m_min"][index]),
                    maximum_temperature=float(daily_data["temperature_2m_max"][index]),
                    precipitation_probability=optional_float(daily_data["precipitation_probability_max"][index]),
                    precipitation_sum=optional_float(daily_data["precipitation_sum"][index]),
                    maximum_wind_speed=optional_float(daily_data["wind_speed_10m_max"][index]),
                    weather_code=weather_code,
                    condition=weather_code_to_condition(weather_code),
                    sunrise=datetime.fromisoformat(str(daily_data["sunrise"][index])),
                    sunset=datetime.fromisoformat(str(daily_data["sunset"][index])),))

    except (KeyError, TypeError, ValueError) as error:
        raise ExternalAPIError("The weather service returned invalid forecast data.") from error

    uses_imperial_units=(query.temperature_unit == "fahrenheit")

    return WeatherDataResponse(latitude=float(response_data.get("latitude",query.latitude,)),
        longitude=float(response_data.get("longitude",query.longitude,)),
        timezone=str(response_data.get("timezone", "GMT")),
        timezone_abbreviation=response_data.get("timezone_abbreviation"),
        temperature_unit=query.temperature_unit,
        wind_speed_unit=("mph" if uses_imperial_units else "kmh"),
        precipitation_unit=("inch" if uses_imperial_units else "mm"),
        current_weather=current_weather,
        forecast=forecast,
    )

async def fetch_weather(query,settings,):
    uses_imperial_units=(query.temperature_unit == "fahrenheit")
    parameters = {"latitude": query.latitude,"longitude": query.longitude,
                  "current": ",".join(["temperature_2m","apparent_temperature","relative_humidity_2m","precipitation","weather_code","wind_speed_10m","is_day",]),
                "daily": ",".join(["weather_code","temperature_2m_max","temperature_2m_min","precipitation_probability_max","precipitation_sum","wind_speed_10m_max","sunrise","sunset",]),
        "temperature_unit": query.temperature_unit,
        "wind_speed_unit": ("mph" if uses_imperial_units else "kmh"),
        "precipitation_unit": ("inch" if uses_imperial_units else "mm"),
        "timezone":"auto",
        "start_date":query.start_date.isoformat(),
        "end_date":query.end_date.isoformat(),
    }

    try:
        async with httpx.AsyncClient(timeout=settings.external_api_timeout_seconds,) as client:
            response = await client.get(settings.forecast_api_url,params=parameters,)
            response.raise_for_status()

    except httpx.TimeoutException as error:
        raise ExternalAPIError("The weather service timed out.") from error

    except httpx.HTTPStatusError as error:
        reason:str | None = None

        try:
            error_data= error.response.json()
            if isinstance(error_data, dict):
                reason= error_data.get("reason")

        except ValueError:
            reason = None
        raise ExternalAPIError(reason or "The weather service rejected the request.") from error

    except httpx.RequestError as error:
        raise ExternalAPIError("The weather service could not be reached.") from error

    try:
        response_data = response.json()

    except ValueError as error:
        raise ExternalAPIError("The weather service returned invalid JSON.") from error

    if not isinstance(response_data, dict):
        raise ExternalAPIError("The weather service returned an unexpected response.")

    return parse_weather_response(response_data=response_data,query=query,)