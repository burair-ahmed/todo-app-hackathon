from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseSettings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")

# Create an instance of the settings
db_settings = DatabaseSettings()
DATABASE_URL = db_settings.DATABASE_URL