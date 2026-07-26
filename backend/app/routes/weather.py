from typing import Annotated
from fastapi import APIRouter,Depends,HTTPException,Query,status
from app.config import Settings, get_settings
from app.exceptions import ExternalAPIError
from app.schemas import ErrorResponse,WeatherDataResponse,WeatherQuery
from app.services.weather_service import fetch_weather
from app.schemas import AirQualityResponse
from app.services.air_quality_service import fetch_air_quality

router = APIRouter(prefix="/api",tags=["Weather"],)

@router.get("/weather",response_model=WeatherDataResponse,
    responses={502: {"model": ErrorResponse,"description": ("The external weather service failed."),},},)

async def get_weather(weather_query: Annotated[WeatherQuery,Query(),],settings: Annotated[Settings,Depends(get_settings),],):
    try:
        return await fetch_weather(query=weather_query,settings=settings,)

    except ExternalAPIError as error:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY,detail=str(error),) from error

@router.get("/air-quality",response_model=AirQualityResponse,
    responses={502: {"model": ErrorResponse,"description":"The external air-quality service failed.",},},)
async def get_air_quality(latitude: Annotated[float,Query(ge=-90, le=90),],
    longitude: Annotated[float,Query(ge=-180, le=180),],settings: Annotated[Settings,Depends(get_settings),],):
    try:
        return await fetch_air_quality(latitude=latitude,longitude=longitude,settings=settings,)
    except ExternalAPIError as error:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY,detail=str(error),) from error