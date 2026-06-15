import asyncio
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.ingestion.fetch_weather import fetch_all_weather
from src.processing.clean_data import process_data
from src.features.scores import calculate_readiness_score
from src.db.repository import save_weather_readings, save_readiness_scores
from .schemas import PipelineRunResponse

router = APIRouter()


@router.post("/run", response_model=PipelineRunResponse)
async def trigger_pipeline(db: Session = Depends(get_db)):
    """
    Triggers a full pipeline run:
    Fetch → Clean → Score → Store
    """
    raw_data = await fetch_all_weather()

    if not raw_data:
        return PipelineRunResponse(
            status="failed",
            cities_fetched=0,
            weather_rows_saved=0,
            readiness_rows_saved=0,
        )

    cleaned_df = process_data(raw_data)
    featured_df = calculate_readiness_score(cleaned_df)

    weather_count = save_weather_readings(cleaned_df, db)
    readiness_count = save_readiness_scores(featured_df, db)

    return PipelineRunResponse(
        status="success",
        cities_fetched=len(raw_data),
        weather_rows_saved=weather_count,
        readiness_rows_saved=readiness_count,
    )
