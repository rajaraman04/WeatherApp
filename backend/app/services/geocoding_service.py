from typing import Any
import httpx
from app.config import Settings
from app.exceptions import ExternalAPIError,LocationNotFoundError
from app.schemas import LocationSearchResult

def convert_geocoding_result(result):
    required_fields= ["name","latitude","longitude",]
    if any(field not in result for field in required_fields):
        return None
    postcodes= result.get("postcodes") or []
    postal_code= (str(postcodes[0]) if postcodes else None)

    return LocationSearchResult(name=result["name"],state=result.get("admin1"),country=result.get("country") or "Unknown",country_code=result.get("country_code"),postal_code=postal_code,latitude=result["latitude"],longitude=result["longitude"],timezone=result.get("timezone"),)

async def search_locations(query,limit,settings,):
    parameters= {"name": query,"count": limit,"language": "en","format": "json",}
    try:
        async with httpx.AsyncClient(timeout=settings.external_api_timeout_seconds,) as client:
            response= await client.get(settings.geocoding_api_url,params=parameters,)
            response.raise_for_status()

    except httpx.TimeoutException as error:
        raise ExternalAPIError("The location service timed out.") from error

    except httpx.HTTPStatusError as error:
        raise ExternalAPIError("The location service returned an unsuccessful response.") from error

    except httpx.RequestError as error:
        raise ExternalAPIError("The location service could not be reached.") from error

    try:
        response_data= response.json()

    except ValueError as error:
        raise ExternalAPIError("The location service returned invalid data.") from error

    raw_results= response_data.get("results", [])

    if not raw_results:
        raise LocationNotFoundError(query)

    locations: list[LocationSearchResult] = []

    for raw_result in raw_results:
        location= convert_geocoding_result(raw_result)

        if location is not None:
            locations.append(location)

    if not locations:
        raise LocationNotFoundError(query)

    return locations