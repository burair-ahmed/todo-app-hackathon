from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List, Annotated
from uuid import UUID
from ..database.database import get_session
from ..models.task import Task, TaskCreate, TaskRead, TaskUpdate, TaskPatch
from ..models.user import User
from ..services.task_service import (
    create_task, get_tasks_by_user, get_task_by_id,
    update_task, patch_task, delete_task, toggle_task_completion
)
from ..middleware.jwt_auth import get_current_user

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

@router.get("/", response_model=List[TaskRead])
def read_tasks(
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get all tasks for the authenticated user."""
    user_id = current_user["user_id"]
    tasks = get_tasks_by_user(session, user_id)
    return tasks


@router.post("/", response_model=TaskRead)
def create_task_endpoint(
    task_create: TaskCreate,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Create a new task for the authenticated user."""
    user_id = current_user["user_id"]
    task = create_task(session, task_create, user_id)
    return task


@router.get("/{task_id}", response_model=TaskRead)
def read_task(
    task_id: UUID,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get a specific task by ID for the authenticated user."""
    user_id = current_user["user_id"]
    task = get_task_by_id(session, task_id, user_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or doesn't belong to user"
        )

    return task


@router.put("/{task_id}", response_model=TaskRead)
def update_task_endpoint(
    task_id: UUID,
    task_update: TaskUpdate,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update a specific task by ID for the authenticated user."""
    user_id = current_user["user_id"]
    task = update_task(session, task_id, task_update, user_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or doesn't belong to user"
        )

    return task


@router.patch("/{task_id}", response_model=TaskRead)
def patch_task_endpoint(
    task_id: UUID,
    task_patch: TaskPatch,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Partially update a specific task by ID for the authenticated user."""
    user_id = current_user["user_id"]
    task = patch_task(session, task_id, task_patch, user_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or doesn't belong to user"
        )

    return task


@router.delete("/{task_id}")
def delete_task_endpoint(
    task_id: UUID,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Delete a specific task by ID for the authenticated user."""
    user_id = current_user["user_id"]
    success = delete_task(session, task_id, user_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or doesn't belong to user"
        )

    return {"message": "Task deleted successfully"}


@router.put("/{task_id}/toggle", response_model=TaskRead)
def toggle_task_completion_endpoint(
    task_id: UUID,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Toggle the completion status of a task for the authenticated user."""
    user_id = current_user["user_id"]
    task = toggle_task_completion(session, task_id, user_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or doesn't belong to user"
        )

    return task