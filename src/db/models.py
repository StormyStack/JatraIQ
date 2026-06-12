from sqlalchemy import Column, Integer, Float, String, DateTime, Text
from sqlalchemy.sql import func
from .database import Base


class WeatherReading(Base):
    """Raw weather snapshot per city per fetch cycle."""

    __tablename__ = "weather_readings"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String(100), nullable=False, index=True)
    fetched_at = Column(String(50), nullable=False)
    temp = Column(Float)
    feels_like = Column(Float)
    humidity = Column(Integer)
    rain_probability = Column(Float)
    weather_main = Column(String(100))
    wind_speed = Column(Float)
    aqi = Column(Integer)
    pm2_5 = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class TravelReadiness(Base):
    """Derived travel readiness scores per city per fetch cycle."""

    __tablename__ = "travel_readiness"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String(100), nullable=False, index=True)
    fetched_at = Column(String(50), nullable=False)
    temp_score = Column(Float)
    humidity_score = Column(Float)
    rain_score = Column(Float)
    aqi_score = Column(Float)
    overall_score = Column(Float)
    category = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
