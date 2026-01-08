from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, Any
from datetime import datetime
import uuid
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB

class ChatKitThread(SQLModel, table=True):
    __tablename__ = "chatkit_threads"

    id: str = Field(primary_key=True, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    metadata_json: Optional[dict] = Field(default_factory=dict, sa_column=Column(JSONB))
    
    # Relationship to Items
    items: List["ChatKitItem"] = Relationship(back_populates="thread")

class ChatKitItem(SQLModel, table=True):
    __tablename__ = "chatkit_items"

    id: str = Field(primary_key=True, index=True)
    thread_id: str = Field(foreign_key="chatkit_threads.id", index=True)
    type: str # user_message, assistant_message, system_message, etc.
    created_at: datetime = Field(default_factory=datetime.utcnow)
    content: Optional[dict] = Field(default=None, sa_column=Column(JSONB)) # Store complex content as JSON
    
    # Relationship to Thread
    thread: Optional[ChatKitThread] = Relationship(back_populates="items")
