import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text

from app.config import settings
from app.database import Base, engine, init_db
from app.routers import alerts, analyses, auth, dashboard, history, profile
from app.utils.logging_config import setup_logging

APP_ROOT = Path(__file__).resolve().parent.parent
for directory in [settings.UPLOAD_DIR, settings.REPORT_DIR, settings.LOG_DIR, settings.MODEL_DIR]:
    (APP_ROOT / directory).mkdir(parents=True, exist_ok=True)

logger = setup_logging()
app = FastAPI(title=settings.APP_NAME, version="1.0.0")

origins = [origin.strip() for origin in settings.CORS_ORIGINS.split(",") if origin.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(analyses.router)
app.include_router(dashboard.router)
app.include_router(history.router)
app.include_router(alerts.router)
app.include_router(profile.router)

init_db()


@app.on_event("startup")
def startup_event():
    init_db()
    logger.info("Application started and database tables ensured.")


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/health/db")
def db_health_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception:
        return JSONResponse(status_code=503, content={"status": "unhealthy", "database": "disconnected"})


@app.exception_handler(500)
async def server_error_handler(_, exc):
    return JSONResponse(status_code=500, content={"success": False, "error": {"code": "SERVER_ERROR", "message": "An internal server error occurred."}})
