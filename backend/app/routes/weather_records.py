import logging
from typing import Annotated
from fastapi import APIRouter,Depends,HTTPException,Request,status,Query
from pymongo.errors import PyMongoError

from app.config import Settings, get_settings
from app.exceptions import ExternalAPIError,LocationNotFoundError
from app.schemas import ErrorResponse,WeatherRecordCreate,WeatherRecordResponse,WeatherRecordUpdate
from app.services.weather_record_service import prepare_weather_record_document
from app.exceptions import ExternalAPIError,InvalidWeatherRecordIdError,LocationNotFoundError,WeatherRecordNotFoundError
from app.services.weather_record_service import prepare_weather_record_document,read_weather_record_by_id,read_weather_records,update_weather_record_by_id

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

@router.get("",response_model=list[WeatherRecordResponse],
    responses={503: {"model": ErrorResponse,"description": "MongoDB is unavailable.",},},)
async def get_weather_records(request: Request,skip: Annotated[int,Query(ge=0,description=("Number of records to skip."),),]=0,
    limit: Annotated[int,Query(ge=1,le=100,description=("Maximum number of records to return."),),]=20,):
    try:
        weather_collection = (request.app.state.weather_collection)
        return await read_weather_records(collection=weather_collection,skip=skip,limit=limit,)

    except (AttributeError, PyMongoError) as error:
        logger.error("Failed to read weather records: %s",error,)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,detail="The database is currently unavailable.",) from error

@router.get("/{record_id}",response_model=WeatherRecordResponse,
        responses={400:{"model": ErrorResponse,"description": ("The MongoDB record ID is invalid."),},
        404:{"model": ErrorResponse,"description": ("The weather record was not found."),},
        503:{"model": ErrorResponse,"description": "MongoDB is unavailable.",},},)
async def get_weather_record(record_id: str,request: Request,):
    try:
        weather_collection = (request.app.state.weather_collection)
        return await read_weather_record_by_id(collection=weather_collection,record_id=record_id,)

    except InvalidWeatherRecordIdError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(f"'{error.record_id}' is not a valid weather record ID."),) from error

    except WeatherRecordNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(f"Weather record '{error.record_id}' was not found."),) from error

    except (AttributeError, PyMongoError) as error:
        logger.error("Failed to read weather record: %s",error,)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,detail="The database is currently unavailable.",) from error

@router.patch("/{record_id}", response_model=WeatherRecordResponse,
    responses={400:{"model": ErrorResponse,"description": ("The MongoDB record ID is invalid."),},
        404:{"model": ErrorResponse,"description": ("The record or requested location was not found."),},
        502:{"model": ErrorResponse,"description": ("An external weather service failed."),},
        503:{"model": ErrorResponse,"description": ("MongoDB is unavailable."),},},)

async def update_weather_record(record_id: str,update_data: WeatherRecordUpdate,request: Request,settings: Annotated[Settings,Depends(get_settings),],):
    try:
        weather_collection = (request.app.state.weather_collection)
        return await update_weather_record_by_id(collection=weather_collection,record_id=record_id,update_data=update_data,settings=settings,)

    except InvalidWeatherRecordIdError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=(f"'{error.record_id}' is not a valid weather record ID."),) from error

    except WeatherRecordNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=(f"Weather record '{error.record_id}' was not found."),) from error

    except LocationNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=(f"No matching location was found for '{error.query}'."),) from error

    except ExternalAPIError as error:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY,detail=str(error),) from error

    except (AttributeError, PyMongoError) as error:
        logger.error("Failed to update weather record: %s",error,)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,detail=("The database is currently unavailable."),) from error
    