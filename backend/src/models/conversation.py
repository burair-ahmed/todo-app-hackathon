from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid

class ConversationBase(SQLModel):
    user_id: str = Field(index=True)  # Using string to match existing user ID format
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

class Conversation(ConversationBase, table=True):
    __tablename__ = "conversations"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    # Relationship to messages
    messages: List["Message"] = Relationship(back_populates="conversation")

class ConversationCreate(ConversationBase):
    pass

class ConversationRead(ConversationBase):
    id: int