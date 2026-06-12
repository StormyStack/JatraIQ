import asyncio
import sys
from src.ingestion.fetch_weather import fetch_all_weather
from src.processing.clean_data import process_data
from src.features.scores import calculate_readiness_score

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

async def main():
    # 1. Ingestion
    raw_data = await fetch_all_weather()
    
    # 2. Processing
    if raw_data:
        cleaned_df = process_data(raw_data)
        
        # 3. Feature Engineering (Travel Readiness)
        featured_df = calculate_readiness_score(cleaned_df)
        
        # Display results (Preview)
        print(featured_df[['city', 'temp', 'humidity', 'rain_probability', 'aqi_score', 'overall_score', 'category']].head())
        
        # Next step: Send to ML Pipeline / Storage
    else:
        print("Pipeline failed at ingestion.")

if __name__ == "__main__":
    asyncio.run(main())