from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://aura_user:aura_password@postgres:5432/aura_db"
    SECRET_KEY: str = "your-super-secret-key-change-this-in-production"
    RESET_DATABASE: bool = False
    DEBUG: bool = False

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()