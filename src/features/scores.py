import pandas as pd
import numpy as np

def calculate_readiness_score(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates Travel Readiness Score based on:
    - Temperature (Target: 22°C)
    - Humidity (Target: 45%)
    - Rain Probability (Target: 0%)
    - AQI (Target: 1, 1-5 scale)
    """
    
    # 1. Temperature Score (100 is best, drops as it moves away from 22°C)
    df['temp_score'] = 100 - abs(df['temp'] - 22) * 5
    df['temp_score'] = df['temp_score'].clip(0, 100)

    # 2. Humidity Score (Target 45%)
    df['humidity_score'] = 100 - abs(df['humidity'] - 45) * 1.5
    df['humidity_score'] = df['humidity_score'].clip(0, 100)

    # 3. Rain Score
    # Assuming 'rain_probability' is a float (0.0 to 1.0)
    # If prob is 0, score is 100. If prob is 1.0 (100%), score is 0.
    df['rain_score'] = (1 - df['rain_probability']) * 100
    df['rain_score'] = df['rain_score'].clip(0, 100)

    # 4. AQI Score
    # AQI is 1 (Good) to 5 (Very Poor).
    df['aqi'] = df['aqi'].fillna(1)
    df['aqi_score'] = 100 - (df['aqi'] - 1) * 25
    df['aqi_score'] = df['aqi_score'].clip(0, 100)

    # 5. Weighted Overall Score
    # We prioritize Rain (30%), Temp (25%), Humidity (25%), and AQI (20%)
    df['overall_score'] = (
        (df['temp_score'] * 0.25) + 
        (df['humidity_score'] * 0.25) + 
        (df['rain_score'] * 0.30) +
        (df['aqi_score'] * 0.20)
    ).round(2)

    # 5. Categorization
    def categorize(score):
        if score >= 80: return "Excellent"
        if score >= 60: return "Good"
        if score >= 40: return "Moderate"
        return "Risky"

    df['category'] = df['overall_score'].apply(categorize)
    
    return df