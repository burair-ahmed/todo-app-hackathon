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
from ..services.agent_service import process_chat_request
from pydantic import BaseModel

router = APIRouter()

class ChatRequest(BaseModel):
    conversation_id: int = None  # Optional - if not provided, create new conversation
    message: str

class ChatResponse(BaseModel):
    conversation_id: int
    response: str
    tool_calls: List[dict] = []

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

    # Process the request with the agent
    agent_response = await process_chat_request(
        user_id=user_id,
        conversation_id=conversation_id,
        user_message=chat_request.message,
        conversation_history=conversation_history
    )

    # Execute any tool calls returned by the agent
    tool_call_results = []
    if agent_response.get("tool_calls"):
        from ..services.agent_service import execute_tool_call
        for tool_call in agent_response["tool_calls"]:
            result = execute_tool_call(tool_call["name"], tool_call["arguments"])
            tool_call_results.append({
                "name": tool_call["name"],
                "result": result
            })

    # Create the assistant message
    assistant_message_data = MessageCreate(
        user_id=user_id,  # The assistant is acting on behalf of the system but associated with the user
        conversation_id=conversation_id,
        role="assistant",
        content=agent_response.get("response", "")
    )
    assistant_message = create_message(session, assistant_message_data)

    return ChatResponse(
        conversation_id=conversation_id,
        response=agent_response.get("response", ""),
        tool_calls=tool_call_results  # Return tool call results
    )

# Additional endpoints for conversation management could be added here