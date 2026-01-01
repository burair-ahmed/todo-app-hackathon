from sqlmodel import create_engine, Session
from .config import DATABASE_URL

# Create the database engine
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session