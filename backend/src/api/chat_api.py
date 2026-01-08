from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlmodel import Session
from ..database import get_session
from ..middleware.jwt_auth import get_current_user
from ..models.conversation import Conversation, ConversationCreate, ConversationRead
from ..models.message import Message, MessageCreate, MessageRead
from ..services.conversation_service import (
    create_conversation,
    get_conversation_by_id,
    update_conversation
)
from ..services.message_service import (
    create_message,
    get_messages_by_conversation_id,
    get_messages_by_user_id
)
from ..services.agent_service import run_agent
from pydantic import BaseModel

router = APIRouter()

class ChatRequest(BaseModel):
    conversation_id: int = None  # Optional - if not provided, create new conversation
    message: str

class ChatResponse(BaseModel):
    conversation_id: int
    response: str
    tool_calls: List[dict] = [] # Kept for schema compatibility, but will be empty

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    user_id: str,
    chat_request: ChatRequest,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Process a chat message in a conversation and return the AI response along with any tool calls.
    """
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"Chat endpoint called for user: {user_id}")
    
    # Verify that the user making the request is the same as the user_id in the path
    if str(current_user["user_id"]) != user_id:
        logger.warning(f"Auth mismatch: token user {current_user['user_id']} vs path user {user_id}")
        raise HTTPException(status_code=403, detail="Not authorized to access this user's conversations")

    logger.info(f"Processing message: {chat_request.message[:50]}...")

    # If no conversation_id provided, create a new conversation
    conversation_id = chat_request.conversation_id
    if not conversation_id:
        conversation_data = ConversationCreate(user_id=user_id)
        conversation = create_conversation(session, conversation_data)
        conversation_id = conversation.id
    else:
        # Verify that the conversation belongs to the user
        conversation = get_conversation_by_id(session, conversation_id)
        if not conversation or conversation.user_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to access this conversation")

        # Update the conversation's updated_at timestamp
        update_conversation(session, conversation_id)

    # Create the user message
    user_message_data = MessageCreate(
        user_id=user_id,
        conversation_id=conversation_id,
        role="user",
        content=chat_request.message
    )
    user_message = create_message(session, user_message_data)

    # Get conversation history for the agent
    conversation_history = get_messages_by_conversation_id(session, conversation_id)
    
    # 1. Format history for run_agent
    history_for_agent = []
    for msg in conversation_history:
        # Avoid including the message we just added (if get_messages includes it)
        # or logic to ensure order. Assuming get_messages returns ordered list.
        # run_agent expects [{"role": "user/assistant", "content": "..."}]
        
        # Mapping: Model Message role "assistant" -> "assistant"
        role = msg.role
        if role not in ["user", "assistant"]:
             continue
             
        history_for_agent.append({
            "role": role,
            "content": msg.content
        })

    # 2. Run Agent (ReAct Loop)
    # The agent now executes tools internally.
    agent_result = await run_agent(
        user_id=user_id,
        user_message=chat_request.message,
        history=history_for_agent
    )
    
    response_text = agent_result.get("response", "")
    # We could also log agent_result.get("tool_trace") if needed for debug

    # Create the assistant message
    assistant_message_data = MessageCreate(
        user_id=user_id,
        conversation_id=conversation_id,
        role="assistant",
        content=response_text
    )
    assistant_message = create_message(session, assistant_message_data)

    return ChatResponse(
        conversation_id=conversation_id,
        response=response_text,
        tool_calls=[] # New agent handles tool calls internally
    )

# Additional endpoints for conversation management could be added here