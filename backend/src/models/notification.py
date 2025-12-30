import uuid
from datetime import datetime
from enum import Enum
from typing import Optional
from sqlmodel import Field, SQLModel

class NotificationType(str, Enum):
    TASK_DUE = "task_due"
    TASK_OVERDUE = "task_overdue"
    RECURRING_SPAWNED = "recurring_spawned"
    GENERAL = "general"

class NotificationBase(SQLModel):
    user_id: uuid.UUID = Field(foreign_key="users.id")
    type: NotificationType = Field(default=NotificationType.GENERAL)
    message: str
    task_id: Optional[uuid.UUID] = Field(default=None, foreign_key="tasks.id")
    is_read: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Notification(NotificationBase, table=True):
    __tablename__ = "notifications"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

class NotificationRead(NotificationBase):
    id: uuid.UUID
