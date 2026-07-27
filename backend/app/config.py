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
    app_timezone:str="America/New_York"
    model_config = SettingsConfigDict(env_file=".env",env_file_encoding="utf-8",case_sensitive=False,extra="ignore",)
    cors_origins: str = ("http://localhost:5173," "http://127.0.0.1:5173," "http://localhost:4173," "http://127.0.0.1:4173")

@property
def cors_origin_list(self):
    return [origin.strip().rstrip("/") for origin in self.cors_origins.split(",") if origin.strip()]

@lru_cache
def get_settings():
    return Settings()
