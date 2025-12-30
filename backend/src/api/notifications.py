from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select, desc
from ..database.database import get_session
from ..models.user import User
from ..models.notification import Notification, NotificationRead
from ..middleware.jwt_auth import get_current_user

router = APIRouter(prefix="/api/notifications", tags=["notifications"])

@router.get("", response_model=List[NotificationRead])
def get_notifications(
    skip: int = 0,
    limit: int = 20,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    """Get notifications for the current user."""
    statement = select(Notification).where(
        Notification.user_id == current_user["user_id"]
    ).order_by(desc(Notification.created_at)).offset(skip).limit(limit)
    
    notifications = session.exec(statement).all()
    return notifications

@router.get("/unread-count", response_model=int)
def get_unread_count(
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    """Get the count of unread notifications."""
    statement = select(Notification).where(
        Notification.user_id == current_user["user_id"],
        Notification.is_read == False
    )
    results = session.exec(statement).all()
    return len(results)

@router.post("/{notification_id}/read", response_model=NotificationRead)
def mark_notification_as_read(
    notification_id: UUID,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    """Mark a notification as read."""
    statement = select(Notification).where(
        Notification.id == notification_id,
        Notification.user_id == current_user["user_id"]
    )
    notification = session.exec(statement).first()
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
        
    notification.is_read = True
    session.add(notification)
    session.commit()
    session.refresh(notification)
    return notification

@router.post("/read-all", response_model=dict)
def mark_all_as_read(
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    """Mark all notifications as read for the user."""
    statement = select(Notification).where(
        Notification.user_id == current_user["user_id"],
        Notification.is_read == False
    )
    notifications = session.exec(statement).all()
    
    for notification in notifications:
        notification.is_read = True
        session.add(notification)
        
    session.commit()
    return {"message": "All marked as read"}
