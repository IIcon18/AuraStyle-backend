from pydantic_settings import BaseSettings
from datetime import timedelta


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://aura_user:aura_password@postgres:5432/aura_db"
    RESET_DATABASE: bool = False

    # Security
    SECRET_KEY: str = "your-super-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # App
    DEBUG: bool = False
    FRONTEND_URL: str = "http://localhost:3000"
    UPLOAD_DIR: str = "uploads"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()