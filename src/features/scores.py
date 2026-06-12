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
    
    df['temp_score'] = 100 - abs(df['temp'] - 22) * 5
    df['temp_score'] = df['temp_score'].clip(0, 100)

    df['humidity_score'] = 100 - abs(df['humidity'] - 45) * 1.5
    df['humidity_score'] = df['humidity_score'].clip(0, 100)

    df['rain_score'] = (1 - df['rain_probability']) * 100
    df['rain_score'] = df['rain_score'].clip(0, 100)

    df['aqi'] = df['aqi'].fillna(1)
    df['aqi_score'] = 100 - (df['aqi'] - 1) * 25
    df['aqi_score'] = df['aqi_score'].clip(0, 100)

    df['overall_score'] = (
        (df['temp_score'] * 0.25) + 
        (df['humidity_score'] * 0.25) + 
        (df['rain_score'] * 0.30) +
        (df['aqi_score'] * 0.20)
    ).round(2)

    def categorize(score):
        if score >= 80: return "Excellent"
        if score >= 60: return "Good"
        if score >= 40: return "Moderate"
        return "Risky"

    df['category'] = df['overall_score'].apply(categorize)
    
    return df