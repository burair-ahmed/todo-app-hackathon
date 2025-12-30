from sqlmodel import Session, select, or_, desc
from typing import List, Optional
from uuid import UUID
from datetime import timedelta
from ..models.task import Task, TaskCreate, TaskUpdate, TaskPatch, Tag, TaskTagLink
from ..models.user import User

def create_task(session: Session, task_create: TaskCreate, user_id: UUID) -> Task:
    """Create a new task for a user with priorities and tags."""
    task = Task(
        title=task_create.title,
        description=task_create.description,
        completed=task_create.completed,
        priority=task_create.priority,
        label=task_create.label,
        due_date=task_create.due_date,
        recurrence=task_create.recurrence,
        user_id=user_id
    )
    
    if task_create.tag_ids:
        statement = select(Tag).where(Tag.id.in_(task_create.tag_ids), Tag.user_id == user_id)
        tags = session.exec(statement).all()
        task.tags = tags

    session.add(task)
    session.commit()
    session.refresh(task)
    return task

def get_tasks_by_user(
    session: Session, 
    user_id: UUID,
    search: Optional[str] = None,
    priority: Optional[str] = None,
    completed: Optional[bool] = None,
    tag_id: Optional[UUID] = None,
    label: Optional[str] = None,
    sort_by: str = "created_at",
    order: str = "desc"
) -> List[Task]:
    """Get all tasks for a specific user with advanced filtering and sorting."""
    statement = select(Task).where(Task.user_id == user_id)
    
    if search:
        statement = statement.where(
            or_(
                Task.title.ilike(f"%{search}%"),
                Task.description.ilike(f"%{search}%")
            )
        )
    
    if priority:
        statement = statement.where(Task.priority == priority)
        
    if completed is not None:
        statement = statement.where(Task.completed == completed)

    if tag_id:
        statement = statement.join(TaskTagLink).where(TaskTagLink.tag_id == tag_id)

    if label:
        statement = statement.where(Task.label == label)

    # Sorting logic
    sort_attr = getattr(Task, sort_by, Task.created_at)
    if order == "desc":
        statement = statement.order_by(desc(sort_attr))
    else:
        statement = statement.order_by(sort_attr)

    tasks = session.exec(statement).all()
    return tasks

def get_task_by_id(session: Session, task_id: UUID, user_id: UUID) -> Optional[Task]:
    """Get a specific task by ID for a specific user."""
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()
    return task

def update_task(session: Session, task_id: UUID, task_update: TaskUpdate, user_id: UUID) -> Optional[Task]:
    """Update a specific task for a user, including priority and tags."""
    task = get_task_by_id(session, task_id, user_id)
    if not task:
        return None

    update_data = task_update.dict(exclude_unset=True)
    
    # Handle tag_ids separately
    tag_ids = update_data.pop("tag_ids", None)
    if tag_ids is not None:
        statement = select(Tag).where(Tag.id.in_(tag_ids), Tag.user_id == user_id)
        tags = session.exec(statement).all()
        task.tags = tags

    for field, value in update_data.items():
        setattr(task, field, value)

    session.add(task)
    session.commit()
    session.refresh(task)
    return task

def patch_task(session: Session, task_id: UUID, task_patch: TaskPatch, user_id: UUID) -> Optional[Task]:
    """Partially update a specific task for a user."""
    task = get_task_by_id(session, task_id, user_id)
    if not task:
        return None

    patch_data = task_patch.dict(exclude_unset=True)
    for field, value in patch_data.items():
        setattr(task, field, value)

    session.add(task)
    session.commit()
    session.refresh(task)
    return task

def delete_task(session: Session, task_id: UUID, user_id: UUID) -> bool:
    """Delete a specific task for a user."""
    task = get_task_by_id(session, task_id, user_id)
    if not task:
        return False

    session.delete(task)
    session.commit()
    return True

def toggle_task_completion(session: Session, task_id: UUID, user_id: UUID) -> Optional[Task]:
    """Toggle the completion status of a specific task with recurrence logic."""
    task = get_task_by_id(session, task_id, user_id)
    if not task:
        return None

    from ..models.task import RecurrenceEnum
    
    # If task is currently being marked as completed (from False to True)
    if not task.completed:
        if task.recurrence and task.recurrence != RecurrenceEnum.NONE:
            # Reschedule if it has a due date
            if task.due_date:
                if task.recurrence == RecurrenceEnum.DAILY:
                    task.due_date = task.due_date + timedelta(days=1)
                elif task.recurrence == RecurrenceEnum.WEEKLY:
                    task.due_date = task.due_date + timedelta(weeks=1)
                elif task.recurrence == RecurrenceEnum.MONTHLY:
                    # Approximation: 30 days. For production, use relativedelta
                    task.due_date = task.due_date + timedelta(days=30)
                
                # We don't mark it completed, just reschedule it
                # Effectively, it stays in the list with a new date
                task.completed = False 
            else:
                # No due date? Just mark as completed
                task.completed = True
        else:
            task.completed = True
    else:
        # Marking a completed task back to uncompleted
        task.completed = False

    session.add(task)
    session.commit()
    session.refresh(task)
    return task