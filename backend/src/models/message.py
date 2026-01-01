from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
from enum import Enum

class MessageRole(str, Enum):
    user = "user"
    assistant = "assistant"

class MessageBase(SQLModel):
    user_id: str = Field(index=True)  # Using string to match existing user ID format
    conversation_id: int = Field(foreign_key="conversations.id", index=True)
    role: MessageRole
    content: str
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

class Message(MessageBase, table=True):
    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    conversation_id: int = Field(foreign_key="conversations.id", index=True)
    role: MessageRole
    content: str = Field(sa_column_kwargs={"nullable": False})
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    # Relationship to conversation
    conversation: "Conversation" = Relationship(back_populates="messages")

class MessageCreate(MessageBase):
    pass

class MessageRead(MessageBase):
    id: int