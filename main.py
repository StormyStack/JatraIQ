from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.db.init_db import init_db
from src.api.routes import router as data_router
from src.api.pipeline import router as pipeline_router
from src.api.scheduler import start_scheduler

app = FastAPI(
    title="JatraIQ API",
    description="Travel-readiness weather intelligence for Bangladesh",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(data_router, prefix="/api/v1", tags=["Weather & Readiness"])
app.include_router(pipeline_router, prefix="/api/v1/pipeline", tags=["Pipeline"])


@app.on_event("startup")
def on_startup():
    init_db()
    start_scheduler()


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "service": "JatraIQ API", "version": "1.0.0"}
