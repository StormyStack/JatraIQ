from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional

from src.db.database import get_db
from src.db.models import WeatherReading, TravelReadiness
from .schemas import WeatherReadingOut, TravelReadinessOut, CitySnapshot

router = APIRouter()


@router.get("/weather", response_model=List[WeatherReadingOut])
def get_weather_readings(
    city: Optional[str] = Query(None, description="Filter by city name"),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Fetch weather readings, optionally filtered by city."""
    query = db.query(WeatherReading).order_by(desc(WeatherReading.created_at))
    if city:
        query = query.filter(WeatherReading.city.ilike(f"%{city}%"))
    return query.limit(limit).all()


@router.get("/weather/{city}", response_model=WeatherReadingOut)
def get_latest_weather(city: str, db: Session = Depends(get_db)):
    """Fetch the most recent weather reading for a specific city."""
    reading = (
        db.query(WeatherReading)
        .filter(WeatherReading.city.ilike(f"%{city}%"))
        .order_by(desc(WeatherReading.created_at))
        .first()
    )
    if not reading:
        raise HTTPException(status_code=404, detail=f"No weather data found for '{city}'")
    return reading


@router.get("/readiness", response_model=List[TravelReadinessOut])
def get_readiness_scores(
    city: Optional[str] = Query(None, description="Filter by city name"),
    category: Optional[str] = Query(None, description="Filter by category"),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Fetch travel readiness scores."""
    query = db.query(TravelReadiness).order_by(desc(TravelReadiness.created_at))
    if city:
        query = query.filter(TravelReadiness.city.ilike(f"%{city}%"))
    if category:
        query = query.filter(TravelReadiness.category.ilike(category))
    return query.limit(limit).all()


@router.get("/snapshot", response_model=List[CitySnapshot])
def get_city_snapshots(db: Session = Depends(get_db)):
    """
    Returns the latest combined weather + readiness snapshot for every city.
    """
    cities = db.query(WeatherReading.city).distinct().all()
    snapshots = []

    for (city_name,) in cities:
        weather = (
            db.query(WeatherReading)
            .filter(WeatherReading.city == city_name)
            .order_by(desc(WeatherReading.created_at))
            .first()
        )
        readiness = (
            db.query(TravelReadiness)
            .filter(TravelReadiness.city == city_name)
            .order_by(desc(TravelReadiness.created_at))
            .first()
        )

        if weather:
            snapshots.append(CitySnapshot(
                city=weather.city,
                fetched_at=weather.fetched_at,
                temp=weather.temp,
                feels_like=weather.feels_like,
                humidity=weather.humidity,
                rain_probability=weather.rain_probability,
                weather_main=weather.weather_main,
                wind_speed=weather.wind_speed,
                aqi=weather.aqi,
                pm2_5=weather.pm2_5,
                overall_score=readiness.overall_score if readiness else None,
                category=readiness.category if readiness else None,
            ))

    return snapshots
