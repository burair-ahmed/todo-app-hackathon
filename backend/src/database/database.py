from sqlmodel import create_engine, Session
from sqlalchemy import URL
from ..config import settings
from typing import Generator

# Database configuration for Neon Serverless PostgreSQL
DATABASE_URL = settings.DATABASE_URL

# Create engine
engine = create_engine(DATABASE_URL, echo=False)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session