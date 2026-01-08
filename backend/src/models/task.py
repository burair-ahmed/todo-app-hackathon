from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid
from enum import Enum
from sqlalchemy import Enum as SAEnum, Column

class PriorityEnum(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class LabelEnum(str, Enum):
    HOME = "home"
    WORK = "work"

class RecurrenceEnum(str, Enum):
    NONE = "none"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"

class TaskTagLink(SQLModel, table=True):
    __tablename__ = "task_tag_links"
    task_id: uuid.UUID = Field(foreign_key="tasks.id", primary_key=True)
    tag_id: uuid.UUID = Field(foreign_key="tags.id", primary_key=True)

class TagBase(SQLModel):
    name: str = Field(min_length=1, max_length=50)

class Tag(TagBase, table=True):
    __tablename__ = "tags"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    tasks: List["Task"] = Relationship(back_populates="tags", link_model=TaskTagLink)

class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    completed_at: Optional[datetime] = Field(default=None)
    priority: Optional[PriorityEnum] = Field(
        default=PriorityEnum.MEDIUM,
        sa_column=Column(SAEnum(PriorityEnum, values_callable=lambda obj: [e.value for e in obj]), nullable=True)
    )
    label: Optional[LabelEnum] = Field(
        default=None,
        sa_column=Column(SAEnum(LabelEnum, values_callable=lambda obj: [e.value for e in obj], nullable=True))
    )
    due_date: Optional[datetime] = Field(default=None)
    recurrence: Optional[RecurrenceEnum] = Field(
        default=RecurrenceEnum.NONE,
        sa_column=Column(SAEnum(RecurrenceEnum, values_callable=lambda obj: [e.value for e in obj]), nullable=True)
    )
    recurrence_group_id: Optional[uuid.UUID] = Field(default=None)

class Task(TaskBase, table=True):
    __tablename__ = "tasks"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to User
    user: Optional["User"] = Relationship(back_populates="tasks")
    
    # Relationship to Tags
    tags: List[Tag] = Relationship(back_populates="tasks", link_model=TaskTagLink)

class TaskCreate(TaskBase):
    tag_ids: Optional[List[uuid.UUID]] = None

class TagRead(TagBase):
    id: uuid.UUID
    user_id: uuid.UUID

class TaskRead(TaskBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    tags: List[TagRead] = []

class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    completed_at: Optional[datetime] = None
    priority: Optional[PriorityEnum] = None
    label: Optional[LabelEnum] = None
    due_date: Optional[datetime] = None
    recurrence: Optional[RecurrenceEnum] = None
    recurrence_group_id: Optional[uuid.UUID] = None
    tag_ids: Optional[List[uuid.UUID]] = None

class TaskPatch(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    completed_at: Optional[datetime] = None
    priority: Optional[PriorityEnum] = None
    label: Optional[LabelEnum] = None
    due_date: Optional[datetime] = None
    recurrence: Optional[RecurrenceEnum] = None
    recurrence_group_id: Optional[uuid.UUID] = None