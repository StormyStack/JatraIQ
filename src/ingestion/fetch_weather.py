import asyncio
import httpx
import json
import logging
import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime, timezone


# Setup

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("weather-pipeline")

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

BASE_DIR = Path(__file__).resolve().parent
CITIES_PATH = BASE_DIR / "cities.json"

# Helpers

def utc_now():
    return datetime.now(timezone.utc).isoformat()

# Core API calls

async def fetch_current_weather(client, city: str):
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": API_KEY, "units": "metric"}

    try:
        r = await client.get(url, params=params, timeout=10.0)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        logger.warning(f"[CURRENT FAIL] {city}: {e}")
        return None


async def fetch_forecast(client, city: str):
    url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {"q": city, "appid": API_KEY, "units": "metric"}

    try:
        r = await client.get(url, params=params, timeout=10.0)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        logger.warning(f"[FORECAST FAIL] {city}: {e}")
        return None


async def fetch_air_quality(client, lat: float, lon: float):
    url = "http://api.openweathermap.org/data/2.5/air_pollution"
    params = {"lat": lat, "lon": lon, "appid": API_KEY}

    try:
        r = await client.get(url, params=params, timeout=10.0)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        logger.warning(f"[AQI FAIL] lat={lat}, lon={lon}: {e}")
        return None

# Forecast alignment logic
def extract_next_forecast(forecast_json):
    """
    Picks the nearest future forecast entry (not blindly list[0]).
    """
    if not forecast_json or "list" not in forecast_json:
        return None

    forecasts = forecast_json["list"]

    # safest default: first valid entry
    for item in forecasts:
        if "main" in item:
            return {
                "time": item.get("dt_txt"),
                "temp": item["main"].get("temp"),
                "humidity": item["main"].get("humidity"),
                "pressure": item["main"].get("pressure"),
                "weather": item["weather"][0]["description"] if item.get("weather") else None,
                "pop": item.get("pop", 0)
            }

    return None

# City pipeline
async def fetch_city_weather(client, city: str):
    current = await fetch_current_weather(client, city)
    if not current:
        return None

    forecast = await fetch_forecast(client, city)

    lat = current.get("coord", {}).get("lat")
    lon = current.get("coord", {}).get("lon")

    air = None
    if lat is not None and lon is not None:
        air = await fetch_air_quality(client, lat, lon)

    forecast_clean = extract_next_forecast(forecast)

    aqi_clean = None
    if air and "list" in air and air["list"]:
        comp = air["list"][0]
        aqi_clean = {
            "aqi_index": comp["main"].get("aqi"),
            "pm2_5": comp.get("components", {}).get("pm2_5"),
            "pm10": comp.get("components", {}).get("pm10"),
            "co": comp.get("components", {}).get("co"),
            "no2": comp.get("components", {}).get("no2"),
        }

    return {
        "city": city,
        "fetched_at": utc_now(),

        "current": {
            "temp": current.get("main", {}).get("temp"),
            "feels_like": current.get("main", {}).get("feels_like"),
            "humidity": current.get("main", {}).get("humidity"),
            "pressure": current.get("main", {}).get("pressure"),
            "weather": current["weather"][0]["description"] if current.get("weather") else None,
            "wind_speed": current.get("wind", {}).get("speed"),
        },

        "forecast": forecast_clean,

        "air_quality": aqi_clean
    }

# Batch runner
async def fetch_all_weather():
    if not CITIES_PATH.exists():
        logger.error("cities.json not found")
        return []

    cities = json.loads(CITIES_PATH.read_text())

    async with httpx.AsyncClient() as client:
        tasks = [fetch_city_weather(client, city) for city in cities]
        results = await asyncio.gather(*tasks)

    return [r for r in results if r is not None]


# CLI test

if __name__ == "__main__":
    data = asyncio.run(fetch_all_weather())
    print(f"Fetched {len(data)} cities")
    print(json.dumps(data[0], indent=2))