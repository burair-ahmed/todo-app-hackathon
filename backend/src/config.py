from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str

    # JWT settings
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24

    # AI API keys
    GEMINI_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None

    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Todo Full-Stack Application"

    # Backend settings
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:3000",  # Frontend URL
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
    ]

    class Config:
        env_file = ".env"
        extra = "ignore"  # Ignore extra environment variables

settings = Settings()