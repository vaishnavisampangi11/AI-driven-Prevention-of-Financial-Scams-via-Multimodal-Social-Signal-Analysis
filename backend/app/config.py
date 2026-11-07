from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Financial Scam Prevention System"
    DATABASE_URL: str = "postgresql+psycopg://postgres:password@localhost:5433/scam_prevention"
    SECRET_KEY: str = "dev-secret-key-change-me"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    CORS_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173,http://localhost:5174,http://127.0.0.1:5174"
    UPLOAD_DIR: str = "uploads"
    REPORT_DIR: str = "reports"
    LOG_DIR: str = "logs"
    MODEL_DIR: str = "models"

    class Config:
        env_file = ".env"


settings = Settings()
