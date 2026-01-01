from sqlmodel import Session, select
from ..models.message import Message, MessageCreate
from typing import List

def create_message(session: Session, message: MessageCreate) -> Message:
    """
    Create a new message in the database
    """
    db_message = Message.model_validate(message)
    session.add(db_message)
    session.commit()
    session.refresh(db_message)
    return db_message

def get_message_by_id(session: Session, message_id: int) -> Message:
    """
    Get a message by its ID
    """
    statement = select(Message).where(Message.id == message_id)
    return session.exec(statement).first()

def get_messages_by_conversation_id(session: Session, conversation_id: int) -> List[Message]:
    """
    Get all messages for a specific conversation
    """
    statement = select(Message).where(Message.conversation_id == conversation_id).order_by(Message.created_at)
    return session.exec(statement).all()

def get_messages_by_user_id(session: Session, user_id: str) -> List[Message]:
    """
    Get all messages for a specific user
    """
    statement = select(Message).where(Message.user_id == user_id).order_by(Message.created_at)
    return session.exec(statement).all()

def delete_message(session: Session, message_id: int) -> bool:
    """
    Delete a message by its ID
    """
    message = get_message_by_id(session, message_id)
    if message:
        session.delete(message)
        session.commit()
        return True
    return False