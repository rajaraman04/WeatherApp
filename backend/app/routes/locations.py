from typing import Annotated
from fastapi import APIRouter,Depends,HTTPException,Query,status
from app.config import Settings, get_settings
from app.exceptions import ExternalAPIError,LocationNotFoundError
from app.schemas import ErrorResponse,LocationSearchResult
from app.services.geocoding_service import search_locations


router = APIRouter(prefix="/api/locations",tags=["Locations"],)

@router.get("/search",response_model=list[LocationSearchResult],
    responses={404: {"model": ErrorResponse,"description": "No matching location was found.",},
        502: {"model": ErrorResponse,"description": "The external geocoding service failed.",},
    },
)

async def search_location(q: Annotated[str,Query(min_length=2,max_length=120,
    description=("City, town, state, country, or postal code to search for."),
    examples=["Binghamton, NY"],),],settings: Annotated[Settings,Depends(get_settings),],
    limit: Annotated[int,Query(ge=1,le=10,description="Maximum number of results.",),] = 5,):

    normalized_query = q.strip()
    if len(normalized_query) < 2:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=("Location must contain at least two non-space characters."),)
    try:
        return await search_locations(query=normalized_query,limit=limit,settings=settings,)

    except LocationNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=(f"No matching location was found for "f"'{error.query}'."),) from error

    except ExternalAPIError as error:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY,detail=str(error),) from error