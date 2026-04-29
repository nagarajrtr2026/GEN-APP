import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI App Generator"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./sql_app.db")
    PORT: int = int(os.getenv("PORT", "8000"))
    AI_PROVIDER: str = os.getenv("AI_PROVIDER", "dummy")
    API_KEY: str = os.getenv("API_KEY", "")

    class Config:
        env_file = ".env"

settings = Settings()