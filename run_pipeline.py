import asyncio
import sys
from src.ingestion.fetch_weather import fetch_all_weather
from src.processing.clean_data import process_data
from src.features.scores import calculate_readiness_score
from src.db.init_db import init_db
from src.db.database import SessionLocal
from src.db.repository import save_weather_readings, save_readiness_scores

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

async def main():
    init_db()

    raw_data = await fetch_all_weather()

    if raw_data:
        cleaned_df = process_data(raw_data)
        featured_df = calculate_readiness_score(cleaned_df)

        db = SessionLocal()
        try:
            save_weather_readings(cleaned_df, db)
            save_readiness_scores(featured_df, db)
        finally:
            db.close()
        
        print(featured_df[['city', 'temp', 'humidity', 'rain_probability', 'aqi_score', 'overall_score', 'category']].head())
    else:
        print("Pipeline failed at ingestion.")

if __name__ == "__main__":
    asyncio.run(main())