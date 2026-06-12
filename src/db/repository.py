import logging
import pandas as pd
from sqlalchemy.orm import Session
from .models import WeatherReading, TravelReadiness

logger = logging.getLogger(__name__)


def save_weather_readings(df: pd.DataFrame, db: Session) -> int:
    """
    Persists cleaned weather data to the weather_readings table.
    Returns the number of rows inserted.
    """
    records = []
    for _, row in df.iterrows():
        records.append(WeatherReading(
            city=row.get("city"),
            fetched_at=row.get("timestamp"),
            temp=row.get("temp"),
            feels_like=row.get("feels_like"),
            humidity=row.get("humidity"),
            rain_probability=row.get("rain_probability"),
            weather_main=row.get("weather_main"),
            wind_speed=row.get("wind_speed"),
            aqi=row.get("aqi"),
            pm2_5=row.get("pm2_5"),
        ))

    db.bulk_save_objects(records)
    db.commit()
    logger.info(f"Saved {len(records)} weather readings.")
    return len(records)


def save_readiness_scores(df: pd.DataFrame, db: Session) -> int:
    """
    Persists travel readiness scores to the travel_readiness table.
    Returns the number of rows inserted.
    """
    records = []
    for _, row in df.iterrows():
        records.append(TravelReadiness(
            city=row.get("city"),
            fetched_at=row.get("timestamp"),
            temp_score=row.get("temp_score"),
            humidity_score=row.get("humidity_score"),
            rain_score=row.get("rain_score"),
            aqi_score=row.get("aqi_score"),
            overall_score=row.get("overall_score"),
            category=row.get("category"),
        ))

    db.bulk_save_objects(records)
    db.commit()
    logger.info(f"Saved {len(records)} readiness scores.")
    return len(records)
