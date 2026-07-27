from fastapi import FastAPI,HTTPException,Request,status
from pymongo.errors import PyMongoError
from fastapi.middleware.cors import CORSMiddleware
from typing import AsyncIterator
import logging
from app.routes.locations import router as locations_router
from contextlib import asynccontextmanager
from typing import AsyncIterator
from app.config import get_settings
from app.database import create_mongodb_client,verify_mongodb_connection
from app.routes.locations import router as locations_router
from app.routes.weather import router as weather_router
from app.routes.weather_records import router as weather_records_router

logger = logging.getLogger(__name__)
settings=get_settings()
@asynccontextmanager
async def lifespan(app):
    mongodb_client= create_mongodb_client(settings)
    try:
        await verify_mongodb_connection(mongodb_client)
        database= mongodb_client[settings.mongodb_database]
        weather_collection= database[settings.mongodb_collection]
        app.state.mongodb_client= mongodb_client
        app.state.database= database
        app.state.weather_collection= weather_collection
        logger.info("MongoDB connection successful.")
        yield

    finally:
        await mongodb_client.close()
        logger.info("MongoDB connection closed.")


app = FastAPI(title="Weather App",description=("A Weather app API for weather retrieval, CRUD operations, and data export."),version="1.0.0",lifespan=lifespan,)

app.add_middleware(CORSMiddleware,allow_origins=settings.cors_origin_list,allow_credentials=False,allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],allow_headers=["Accept","Content-Type", "Authorization"],expose_headers=["Content-Disposition"])
app.include_router(locations_router)
app.include_router(weather_router)
app.include_router(weather_records_router)

@app.get("/", tags=["General"])
async def root():
    return {
        "message": "Welcome to the Weather App API!",
        "documentation": "/docs",
    }

@app.get("/api/health", tags=["General"])
async def health_check(request:Request):
    try:
        mongodb_client = request.app.state.mongodb_client
        await verify_mongodb_connection(mongodb_client)
    except (AttributeError, PyMongoError) as error:
        logger.error("MongoDB health check failed: %s", error)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,detail="MongoDB is currently unavailable.",) from error
    return {"status": "healthy","service": "Weather App API","version": "1.0.0","database": "connected",}
