from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from uuid import UUID
from ..database.database import get_session
from ..models.task import Tag, TagBase, TagRead
from ..services.tag_service import (
    create_tag, get_tags_by_user, get_tag_by_id, delete_tag
)
from ..middleware.jwt_auth import get_current_user

router = APIRouter(prefix="/api/tags", tags=["tags"])

@router.get("", response_model=List[TagRead])
def read_tags(
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    user_id = current_user["user_id"]
    return get_tags_by_user(session, user_id)

@router.post("", response_model=TagRead)
def create_tag_endpoint(
    tag_create: TagBase,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Create a new tag for the authenticated user."""
    user_id = current_user["user_id"]
    return create_tag(session, tag_create, user_id)

@router.delete("/{tag_id}")
def delete_tag_endpoint(
    tag_id: UUID,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Delete a specific tag for the authenticated user."""
    user_id = current_user["user_id"]
    if not delete_tag(session, tag_id, user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found or doesn't belong to user"
        )
    return {"message": "Tag deleted successfully"}

