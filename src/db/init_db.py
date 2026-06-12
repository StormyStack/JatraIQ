import logging
from .database import Base, engine

logger = logging.getLogger(__name__)


def init_db():
    """Creates all tables in NeonDB if they do not already exist."""
    logger.info("Initializing database schema...")
    Base.metadata.create_all(bind=engine)
    logger.info("Schema ready.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    init_db()
