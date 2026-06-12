import pandas as pd
import logging

# Setup logging
logger = logging.getLogger(__name__)

def validate_weather_data(df: pd.DataFrame) -> pd.DataFrame:
    """Applies validation rules and cleaning."""
    
    # 1. Remove Duplicates (id must be kept before we select final columns)
    if 'id' in df.columns:
        df = df.drop_duplicates(subset=['id'])
    
    # 2. Handle Missing Values (Example: drop rows with critical missing data)
    df = df.dropna(subset=['temp', 'humidity'])
    
    # 3. Validation Rules (Filtering)
    # Temperature: -5 to 50°C
    df = df[(df['temp'] >= -5) & (df['temp'] <= 50)]
    
    # Humidity: 0 to 130%
    df = df[(df['humidity'] >= 0) & (df['humidity'] <= 130)]
    
    return df

def process_data(raw_data: list):
    """
    Main entry point for the processing layer.
    Converts list of JSON dicts to a cleaned DataFrame.
    """
    if not raw_data:
        logger.warning("No data to process.")
        return None
    
    # Normalize nested JSON structure
    df = pd.json_normalize(raw_data)
    
    # Rename columns to match what the ML pipeline expects
    rename_mapping = {
        'fetched_at': 'timestamp',
        'current.temp': 'temp',
        'current.feels_like': 'feels_like',
        'current.humidity': 'humidity',
        'current.weather': 'weather_main',
        'current.wind_speed': 'wind_speed',
        'forecast.pop': 'rain_probability',
        'air_quality.aqi_index': 'aqi',
        'air_quality.pm2_5': 'pm2_5'
    }
    df = df.rename(columns=rename_mapping)
    
    # Apply Validation
    cleaned_df = validate_weather_data(df)
    
    # Convert ISO timestamp to a readable datetime format (without seconds)
    if 'timestamp' in cleaned_df.columns:
        cleaned_df['timestamp'] = pd.to_datetime(cleaned_df['timestamp']).dt.strftime('%Y-%m-%d %H:%M')
        
    # Keep only requested columns for ML (visibility is no longer fetched)
    columns_to_keep = ['city', 'timestamp', 'temp', 'feels_like', 'humidity', 'rain_probability', 'weather_main', 'wind_speed', 'aqi', 'pm2_5']
    cleaned_df = cleaned_df[[col for col in columns_to_keep if col in cleaned_df.columns]]
    
    logger.info(f"Processing complete. {len(cleaned_df)} records validated.")
    return cleaned_df