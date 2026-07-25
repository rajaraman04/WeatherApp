import logging
from typing import Annotated
from fastapi import APIRouter,Depends,HTTPException,Request,status
from pymongo.errors import PyMongoError

from app.config import Settings, get_settings
from app.exceptions import ExternalAPIError,LocationNotFoundError
from app.schemas import ErrorResponse,WeatherRecordCreate,WeatherRecordResponse
from app.services.weather_record_service import prepare_weather_record_document

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/weather-records",tags=["Weather Records"],)

@router.post("",status_code=status.HTTP_201_CREATED,response_model=WeatherRecordResponse,
    responses={
        404:{"model": ErrorResponse,"description":"The location could not be found.",},
        502:{"model": ErrorResponse,"description":("An external weather service failed."),},
        503:{"model": ErrorResponse,"description": "MongoDB is unavailable.",},},)

async def create_weather_record(request_data: WeatherRecordCreate,request: Request,settings: Annotated[Settings,Depends(get_settings),],):
    try:
        weather_document = await prepare_weather_record_document(request_data=request_data,settings=settings,)
        weather_collection = request.app.state.weather_collection
        insert_result = await weather_collection.insert_one(weather_document)

    except LocationNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No matching location was found for '{error.query}'.",) from error

    except ExternalAPIError as error:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY,detail=str(error),) from error

    except (AttributeError, PyMongoError) as error:
        logger.error("Failed to save weather record: %s", error)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,detail="The database is currently unavailable.",) from error
    response_data = {**weather_document,"id": str(insert_result.inserted_id),}

    return WeatherRecordResponse.model_validate(response_data)