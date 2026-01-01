"""
Migration script for chatbot models: Conversation and Message
This should be integrated with Alembic for proper database migrations
"""

# This is a conceptual migration file
# In practice, you would use Alembic to generate and run migrations

from sqlmodel import SQLModel
from backend.src.models.conversation import Conversation
from backend.src.models.message import Message

# Create all tables
def create_chatbot_tables(engine):
    """
    Create Conversation and Message tables in the database
    """
    SQLModel.metadata.create_all(engine)
    print("Conversation and Message tables created successfully")

# This would typically be run as part of the application startup
# or as part of an Alembic migration