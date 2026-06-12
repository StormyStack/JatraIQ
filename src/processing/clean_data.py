import pandas as pd
import logging

logger = logging.getLogger(__name__)

def validate_weather_data(df: pd.DataFrame) -> pd.DataFrame:
    """Applies validation rules and cleaning."""
    if 'id' in df.columns:
        df = df.drop_duplicates(subset=['id'])
    
    df = df.dropna(subset=['temp', 'humidity'])
    df = df[(df['temp'] >= -5) & (df['temp'] <= 50)]
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
    
    df = pd.json_normalize(raw_data)
    
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
    
    cleaned_df = validate_weather_data(df)
    
    if 'timestamp' in cleaned_df.columns:
        cleaned_df['timestamp'] = pd.to_datetime(cleaned_df['timestamp']).dt.strftime('%Y-%m-%d %H:%M')
        
    columns_to_keep = ['city', 'timestamp', 'temp', 'feels_like', 'humidity', 'rain_probability', 'weather_main', 'wind_speed', 'aqi', 'pm2_5']
    cleaned_df = cleaned_df[[col for col in columns_to_keep if col in cleaned_df.columns]]
    
    logger.info(f"Processing complete. {len(cleaned_df)} records validated.")
    return cleaned_df