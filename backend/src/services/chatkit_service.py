import os
from datetime import datetime
from typing import Any, List, Dict
from chatkit.server import ChatKitServer
from chatkit.types import (
    AssistantMessageItem,
    AssistantMessageContent,
    HiddenContextItem,
    ThreadItemAddedEvent,
    ThreadItemDoneEvent,
    ErrorEvent
)
from ..models.message import Message as DBMessage
from .agent_service import run_agent 
from .sql_chatkit_store import SQLChatKitStore

from ..config import settings

class GeminiChatKitServer(ChatKitServer):
    def __init__(self):
        # Initialize with the SQLChatKitStore
        super().__init__(store=SQLChatKitStore())
        
        # We no longer initialize genai directly here.
        # The agent_service handles the client connection.
        pass

    async def respond(self, thread, input_user_message, context) -> Any:
        try:
            # 1. Load History
            # For simplicity, let's load the last 20 messages
            page = await self.store.load_thread_items(thread.id, None, 50, "asc", context)
            items = page.data

            # 2. Convert ChatKit items to OpenAI/Agent history format
            history_for_agent = []
            user_message_text = ""
            
            # Extract text from the latest user message object
            if input_user_message and input_user_message.content:
                 parts = []
                 for c in input_user_message.content:
                     if hasattr(c, 'text'):
                         parts.append(c.text)
                 if parts:
                     user_message_text = "\n".join(parts)

            for item in items:
                # Avoid duplicating the current user message if it's already in the DB list
                if item.type == "user_message" and hasattr(item, "id") and input_user_message and getattr(input_user_message, "id", None) == item.id:
                    continue

                role = "user" if item.type == "user_message" else "assistant" if item.type == "assistant_message" else "tool" if item.type == "hidden_context_item" else None
                
                # We map hidden context items (tool traces) to "tool" role or just exclude/consolidate?
                # Ideally, for a clean history, we just show user and assistant exchanges. 
                # The agent service rebuilds context from fresh or we can pass some context.
                # Simplification: Only pass User/Assistant turns to the agent history.
                if not role or role not in ["user", "assistant"]:
                    continue
                
                content = ""
                if hasattr(item, 'content'):
                    if isinstance(item.content, list):
                        parts = [c.text for c in item.content if hasattr(c, 'text')]
                        content = "\n".join(parts)
                    else:
                        content = str(item.content)
                
                if content:
                    history_for_agent.append({
                        "role": role,
                        "content": content
                    })

            # If implicit user message logic above failed, fallback
            if not user_message_text and history_for_agent and history_for_agent[-1]["role"] == "user":
                 user_message_text = history_for_agent[-1]["content"]
            
            # If no user message found (e.g. initial empty thread), just return greeting
            if not user_message_text:
                 item_id = self.store.generate_item_id("message", thread, context)
                 assistant_item = AssistantMessageItem(
                    id=item_id,
                    thread_id=thread.id,
                    created_at=datetime.now(),
                    content=[AssistantMessageContent(text="How can I help you?")]
                 )
                 yield ThreadItemAddedEvent(item=assistant_item)
                 yield ThreadItemDoneEvent(item=assistant_item)
                 return

            # 3. RUN AGENT
            user_id = context.get("user_id", "default_user")
            
            agent_result = await run_agent(
                user_id=user_id,
                user_message=user_message_text,
                history=history_for_agent
            )
            
            response_text = agent_result.get("response", "No response generated.")
            tool_trace = agent_result.get("tool_trace", "")
            
            # 4. Yield Response (Visible)
            item_id = self.store.generate_item_id("message", thread, context)
            assistant_item = AssistantMessageItem(
                id=item_id,
                thread_id=thread.id,
                created_at=datetime.now(),
                content=[AssistantMessageContent(text=response_text, annotations=[])]
            )
            yield ThreadItemAddedEvent(item=assistant_item)
            yield ThreadItemDoneEvent(item=assistant_item)

            # 5. Yield Trace (Hidden)
            if tool_trace:
                hidden_id = f"hidden_{item_id}"
                hidden_item = HiddenContextItem(
                    id=hidden_id,
                    thread_id=thread.id,
                    created_at=datetime.now(),
                    content=tool_trace
                )
                yield ThreadItemAddedEvent(item=hidden_item)
                yield ThreadItemDoneEvent(item=hidden_item)

        except Exception as e:
            import traceback
            traceback.print_exc()
            try:
                yield ErrorEvent(message=f"An error occurred: {str(e)}")
            except:
                pass
