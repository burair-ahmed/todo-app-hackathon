from sqlmodel import Session, select
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from ..models.task import Tag, TagBase

def create_tag(session: Session, tag_create: TagBase, user_id: UUID) -> Tag:
    """Create a new tag for a user."""
    tag = Tag(
        name=tag_create.name,
        user_id=user_id,
        created_at=datetime.utcnow()
    )
    session.add(tag)
    session.commit()
    session.refresh(tag)
    return tag

def get_tags_by_user(session: Session, user_id: UUID) -> List[Tag]:
    """Get all tags for a specific user."""
    statement = select(Tag).where(Tag.user_id == user_id)
    tags = session.exec(statement).all()
    return tags

def get_tag_by_id(session: Session, tag_id: UUID, user_id: UUID) -> Optional[Tag]:
    """Get a specific tag by ID for a user."""
    statement = select(Tag).where(Tag.id == tag_id, Tag.user_id == user_id)
    tag = session.exec(statement).first()
    return tag

def delete_tag(session: Session, tag_id: UUID, user_id: UUID) -> bool:
    """Delete a specific tag for a user."""
    tag = get_tag_by_id(session, tag_id, user_id)
    if not tag:
        return False
    session.delete(tag)
    session.commit()
    return True
