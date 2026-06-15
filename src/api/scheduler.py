import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from src.ingestion.fetch_weather import fetch_all_weather
from src.processing.clean_data import process_data
from src.features.scores import calculate_readiness_score
from src.db.repository import save_weather_readings, save_readiness_scores
from src.db.database import SessionLocal
from src.integrations.google_sheets import update_google_sheet

logger = logging.getLogger("scheduler")

async def run_automated_pipeline():
    """Scheduled task to run the full pipeline automatically."""
    logger.info("--- Starting Automated Pipeline Run ---")
    
    raw_data = await fetch_all_weather()
    if not raw_data:
        logger.warning("Automated pipeline aborted: No data fetched.")
        return

    cleaned_df = process_data(raw_data)
    featured_df = calculate_readiness_score(cleaned_df)

    db = SessionLocal()
    try:
        w_count = save_weather_readings(cleaned_df, db)
        r_count = save_readiness_scores(featured_df, db)
        logger.info(f"Automated pipeline success: Saved {w_count} weather / {r_count} readiness rows.")
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to save automated pipeline run: {e}")
    finally:
        db.close()

    try:
        logger.info("Syncing data to Google Sheets...")
        success = update_google_sheet(featured_df)
        if success:
            logger.info("Successfully synced data to Google Sheets.")
        else:
            logger.warning("Google Sheets sync completed with failure/skip.")
    except Exception as e:
        logger.error(f"Error updating Google Sheets: {e}")

def start_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        run_automated_pipeline,
        trigger=IntervalTrigger(hours=4),
        id="hourly_pipeline_job",
        name="Fetch and store weather readiness every 4 hours",
        replace_existing=True,
    )
    scheduler.start()
    logger.info("APScheduler started! Pipeline will run automatically every 4 hours.")
