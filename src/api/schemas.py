from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class WeatherReadingOut(BaseModel):
    id: int
    city: str
    fetched_at: str
    temp: Optional[float]
    feels_like: Optional[float]
    humidity: Optional[int]
    rain_probability: Optional[float]
    weather_main: Optional[str]
    wind_speed: Optional[float]
    aqi: Optional[int]
    pm2_5: Optional[float]
    created_at: Optional[datetime]

    model_config = {"from_attributes": True}


class TravelReadinessOut(BaseModel):
    id: int
    city: str
    fetched_at: str
    temp_score: Optional[float]
    humidity_score: Optional[float]
    rain_score: Optional[float]
    aqi_score: Optional[float]
    overall_score: Optional[float]
    category: Optional[str]
    created_at: Optional[datetime]

    model_config = {"from_attributes": True}


class CitySnapshot(BaseModel):
    """Combined view: latest weather + readiness for a single city."""
    city: str
    fetched_at: str
    temp: Optional[float]
    feels_like: Optional[float]
    humidity: Optional[int]
    rain_probability: Optional[float]
    weather_main: Optional[str]
    wind_speed: Optional[float]
    aqi: Optional[int]
    pm2_5: Optional[float]
    overall_score: Optional[float]
    category: Optional[str]


class PipelineRunResponse(BaseModel):
    status: str
    cities_fetched: int
    weather_rows_saved: int
    readiness_rows_saved: int
