import os
from datetime import datetime
from typing import Any, List, Dict
from chatkit.server import ChatKitServer
import google.generativeai as genai
from ..models.message import Message as DBMessage
from .agent_service import detect_tool_calls, execute_tool_call
from .simple_store import SimpleMemoryStore
from chatkit.types import ThreadItemAddedEvent, ThreadItemDoneEvent, AssistantMessageItem, AssistantMessageContent, ErrorEvent
from ..config import settings

# Initialize Gemini
GEMINI_API_KEY = settings.GEMINI_API_KEY
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel('gemini-flash-latest')

class GeminiChatKitServer(ChatKitServer):
    def __init__(self):
        # Initialize with the SimpleMemoryStore
        super().__init__(store=SimpleMemoryStore())

    async def respond(self, thread, input_user_message, context) -> Any:
        """
        Handle incoming messages from ChatKit and generate a response using Gemini.
        """
        try:
            # Load thread items to build history
            # thread is ThreadMetadata, so we use thread.id
            # Note: We need to import DEFAULT_PAGE_SIZE or just use a large number/pagination loop
            # For simplicity, let's load the last 20 messages
            page = await self.store.load_thread_items(thread.id, None, 50, "asc", context)
            items = page.data

            # Convert ChatKit items to Gemini history format
            history_for_ai = []
            user_message = ""
            
            if input_user_message and input_user_message.content:
                 # Extract text from the latest user message
                 # UserMessageItem content is List[UserMessageContent]
                 parts = []
                 for c in input_user_message.content:
                     if hasattr(c, 'text'):
                         parts.append(c.text)
                 if parts:
                     user_message = "\n".join(parts)

            for item in items:
                role = "user" if item.type == "user_message" else "model" if item.type == "assistant_message" else None
                if not role:
                    continue
                
                parts = []
                # Check different content structures based on item type
                if hasattr(item, 'content'):
                    # AssistantMessageItem and UserMessageItem have content list
                    for c in item.content:
                        if hasattr(c, 'text'):
                            parts.append(c.text)
                
                if parts:
                    history_for_ai.append({
                        "role": role,
                        "parts": parts
                    })

            # If implicit user message logic above failed, fallback or just rely on history
            if not user_message and history_for_ai and history_for_ai[-1]["role"] == "user":
                 user_message = "\n".join(history_for_ai[-1]["parts"])
            
            # If no user message found (e.g. initial empty thread), just return
            if not user_message:
                 # It might be an initial load or empty
                 yield {
                    "type": "assistant_message",
                    "id": self.store.generate_item_id("message", thread, context),
                    "thread_id": thread.id,
                    "created_at": str(datetime.now()),
                    "content": [{"type": "text", "text": "How can I help you?"}]
                 }
                 return

            # Prepare user input with instructions (reusing logic from agent_service)
            user_id = context.get("user_id", "default_user") if isinstance(context, dict) else "default_user"

            user_input_with_instructions = f"""
            User (ID: {user_id}): {user_message}

            Instructions for you:
            - If the user wants to add a task, respond with a structured JSON indicating the add_task tool call
            - If the user wants to list tasks, respond with a structured JSON indicating the list_tasks tool call
            - If the user wants to update a task, respond with a structured JSON indicating the update_task tool call
            - If the user wants to complete a task, respond with a structured JSON indicating the complete_task tool call
            - If the user wants to delete a task, respond with a structured JSON indicating the delete_task tool call
            - Only use these tools when the user explicitly requests task management operations
            - For other questions, respond normally without tool calls
            """
            
            # Call Gemini
            # We filter history to exclude the VERY last message if it matches user_message to avoid duplication 
            # if we pass it explicitly, OR we just pass history.
            # Gemini start_chat history expectation: list of Content objects.
            # We'll use the history *excluding the current message* if we can identify it.
            
            # Simplest approach: Pass empty history and include full context in prompt? No, we want chat context.
            # Let's filter out the last message if it's the user input key
            past_history = [h for h in history_for_ai if "\n".join(h["parts"]) != user_message]

            try:
                chat = gemini_model.start_chat(history=past_history)
                response = chat.send_message(user_input_with_instructions)
                ai_text = response.text
            except Exception as e:
                ai_text = f"Error communicating with Gemini: {str(e)}"

            # Detect and Execute Tools
            tool_calls = detect_tool_calls(ai_text, user_message, user_id)
            
            final_response_text = ai_text
            
            if tool_calls:
                results_text = "\n\nTool Execution Results:"
                for tool in tool_calls:
                    result = execute_tool_call(tool["name"], tool["arguments"])
                    results_text += f"\n- {tool['name']}: {result}"
                final_response_text += results_text

            item_id = self.store.generate_item_id("message", thread, context)
            assistant_item = AssistantMessageItem(
                id=item_id,
                thread_id=thread.id,
                created_at=datetime.now(),
                content=[AssistantMessageContent(text=final_response_text, annotations=[])]
            )
            
            yield ThreadItemAddedEvent(item=assistant_item)
            yield ThreadItemDoneEvent(item=assistant_item)

        except Exception as e:
            # Log error
            import traceback
            traceback.print_exc()
            
            # Use specific ErrorEvent for failures
            try:
                yield ErrorEvent(message=f"An error occurred: {str(e)}")
            except:
                pass
