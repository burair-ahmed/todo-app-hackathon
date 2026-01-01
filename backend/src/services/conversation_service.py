from sqlmodel import Session, select
from ..models.conversation import Conversation, ConversationCreate
from datetime import datetime
from uuid import UUID

def create_conversation(session: Session, conversation: ConversationCreate) -> Conversation:
    """
    Create a new conversation in the database
    """
    db_conversation = Conversation.from_orm(conversation) if hasattr(Conversation, 'from_orm') else Conversation.model_validate(conversation)
    session.add(db_conversation)
    session.commit()
    session.refresh(db_conversation)
    return db_conversation

def get_conversation_by_id(session: Session, conversation_id: int) -> Conversation:
    """
    Get a conversation by its ID
    """
    statement = select(Conversation).where(Conversation.id == conversation_id)
    return session.exec(statement).first()

def get_conversations_by_user_id(session: Session, user_id: str) -> list[Conversation]:
    """
    Get all conversations for a specific user
    """
    statement = select(Conversation).where(Conversation.user_id == user_id)
    return session.exec(statement).all()

def update_conversation(session: Session, conversation_id: int) -> Conversation:
    """
    Update a conversation's updated_at timestamp
    """
    conversation = get_conversation_by_id(session, conversation_id)
    if conversation:
        conversation.updated_at = datetime.utcnow()
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
    return conversation

def delete_conversation(session: Session, conversation_id: int) -> bool:
    """
    Delete a conversation by its ID
    """
    conversation = get_conversation_by_id(session, conversation_id)
    if conversation:
        session.delete(conversation)
        session.commit()
        return True
    return False