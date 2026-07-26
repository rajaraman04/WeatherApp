from functools import lru_cache
from pydantic_settings import BaseSettings,SettingsConfigDict
class Settings(BaseSettings):
    mongodb_uri:str
    mongodb_database:str="WeatherApp"
    mongodb_collection:str="Weather_records"
    geocoding_api_url:str="https://geocoding-api.open-meteo.com/v1/search"
    forecast_api_url:str="https://api.open-meteo.com/v1/forecast"
    air_quality_api_url: str = "https://air-quality-api.open-meteo.com/v1/air-quality"
    external_api_timeout_seconds: float = 10.0
    model_config = SettingsConfigDict(env_file=".env",env_file_encoding="utf-8",case_sensitive=False,extra="ignore",)

@lru_cache
def get_settings():
    return Settings()
