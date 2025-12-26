from sqlmodel import Session, select
from typing import List, Optional
from uuid import UUID
from ..models.task import Task, TaskCreate, TaskUpdate, TaskPatch
from ..models.user import User

def create_task(session: Session, task_create: TaskCreate, user_id: UUID) -> Task:
    """Create a new task for a user."""
    task = Task(
        title=task_create.title,
        description=task_create.description,
        completed=task_create.completed,
        user_id=user_id
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

def get_tasks_by_user(session: Session, user_id: UUID) -> List[Task]:
    """Get all tasks for a specific user."""
    statement = select(Task).where(Task.user_id == user_id)
    tasks = session.exec(statement).all()
    return tasks

def get_task_by_id(session: Session, task_id: UUID, user_id: UUID) -> Optional[Task]:
    """Get a specific task by ID for a specific user."""
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()
    return task

def update_task(session: Session, task_id: UUID, task_update: TaskUpdate, user_id: UUID) -> Optional[Task]:
    """Update a specific task for a user."""
    task = get_task_by_id(session, task_id, user_id)
    if not task:
        return None

    update_data = task_update.dict(exclude_unset=True)
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
    """Toggle the completion status of a specific task for a user."""
    task = get_task_by_id(session, task_id, user_id)
    if not task:
        return None

    task.completed = not task.completed
    session.add(task)
    session.commit()
    session.refresh(task)
    return task