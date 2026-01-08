import os
import re
from datetime import datetime
from typing import Any, List, Dict
from chatkit.server import ChatKitServer
import google.generativeai as genai
from ..models.message import Message as DBMessage
from .agent_service import detect_tool_calls, execute_tool_call
from .simple_store import SimpleMemoryStore
from chatkit.types import (
    ThreadItemAddedEvent, 
    ThreadItemDoneEvent, 
    AssistantMessageItem, 
    AssistantMessageContent, 
    ErrorEvent,
    HiddenContextItem
)
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
                # If we're at the very end and this matches our current input, don't double-add
                if item.type == "user_message" and hasattr(item, "id") and input_user_message and getattr(input_user_message, "id", None) == item.id:
                    continue

                role = "user" if item.type == "user_message" else "model" if item.type in ["assistant_message", "hidden_context_item"] else None
                if not role:
                    continue
                
                parts = []
                if item.type == "hidden_context_item" and hasattr(item, "content"):
                    # Wrap hidden content in a VERY clear boundary for AI
                    parts.append(f"--- INTERNAL CONTEXT (DO NOT SHOW TO USER) ---\n{item.content}\n--- END INTERNAL CONTEXT ---")
                elif hasattr(item, 'content'):
                    if isinstance(item.content, list):
                        for c in item.content:
                            if hasattr(c, 'text'):
                                parts.append(c.text)
                    else:
                        parts.append(str(item.content))
                
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

            # Pass 1: Get Tool Calls
            # We already have history_for_ai from database.
            user_id = context.get("user_id", "default_user")
            
            # We'll prepend a system instruction if it's the first message or just use the current one.
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            current_user_prompt = f"""
            Current Local Time: {current_time}
            User (ID: {user_id}): {user_message}

            System Instructions:
            - You are the Task Management Assistant.
            - I have provided your previous tool execution results in the chat history between "INTERNAL CONTEXT" markers.
            
            TIME AWARENESS:
            - Use the "Current Local Time" provided above as the ABSOLUTE basis for all relative terms (e.g., "today", "tomorrow", "next Friday").
            - If today is Jan 1st, 2026, then "tomorrow" is Jan 2nd, 2026.
            - ALWAYS output the `due_date` in ISO format (YYYY-MM-DDTHH:MM:SS).
            
            TOOL USAGE RULES:
            - To perform an action, output EXACTLY one block like: [JSON: {{"name": "tool_name", "arguments": {{"user_id": "{user_id}", ...}} }}]
            - If the user says "Task 1", refer to the 1st task ID in the most recent `list_tasks` result found in that internal context.
            - You MUST output the EXACT UUID in your [JSON: ...] tool call.
            
            TASK CREATION & UPDATING:
            - The `add_task` and `update_task` tools now support these fields:
              * `priority`: "low", "medium", "high"
              * `label`: "work", "home"
              * `due_date`: e.g. "2026-01-02T14:00:00"
              * `recurrence`: "none", "daily", "weekly", "monthly"
            - Be interactive! If a user is vague (e.g., "Add a task to buy milk"), you can add it, but also ask if they want to set a priority, a due date, or a label (work/home).
            - If the user provides details like "Due tomorrow" or "at work", map those to the correct tool arguments.
            
            GENERAL RULES:
            - DO NOT tell the user about UUIDs or the hidden memory.
            - Provide a friendly text response along with your tool call.
            """

            try:
                chat = gemini_model.start_chat(history=history_for_ai)
                response = chat.send_message(current_user_prompt)
                ai_text = response.text
            except Exception as e:
                ai_text = f"Error communicating with Gemini: {str(e)}"

            # Detect and Execute Tools
            tool_calls = detect_tool_calls(ai_text, user_message, user_id)
            
            # Pass 2: Finalize text and internal memory
            final_response_text = ai_text
            internal_memory_text = ai_text # What Gemini will see in next turn
            
            if tool_calls:
                # Pass 2: Summarize Results
                tool_results_summary = ""
                for tool in tool_calls:
                    result = await execute_tool_call(tool["name"], tool["arguments"])
                    tool_results_summary += f"\nTool '{tool['name']}' Result: {result}"
                
                # Ask Gemini to summarize the combined state
                summary_prompt = f"""
                The user requested: "{user_message}"
                You decided to use these tools. Here are the execution results:
                {tool_results_summary}
                
                Now, provide a clean, human-friendly summary to the user.
                - If you listed tasks, show them in a clean numbered list (e.g., 1. Buy Milk).
                - DO NOT show task UUIDs unless the user specifically needs them.
                - DO NOT mention "JSON" or "Tools" in your final response.
                - Be conversational and helpful.
                """
                try:
                    # We continue the same chat to maintain context
                    summary_response = chat.send_message(summary_prompt)
                    final_response_text = summary_response.text
                    # Internal memory should include both the summary AND the raw tool results
                    internal_memory_text = f"{final_response_text}\n\n[INTERNAL_SYSTEM_DATA: TOOL_RESULTS]\n{tool_results_summary}"
                except Exception as e:
                    final_response_text += f"\n(Summary failed: {str(e)})"
                    internal_memory_text = final_response_text

            # Clean output for UI: Remove any [JSON: ...] blocks
            clean_ui_text = re.sub(r"\[JSON:.*?\]", "", final_response_text, flags=re.DOTALL).strip()
            
            # 1. Yield the UI message (Clean text, no technical bits)
            item_id = self.store.generate_item_id("message", thread, context)
            assistant_item = AssistantMessageItem(
                id=item_id,
                thread_id=thread.id,
                created_at=datetime.now(),
                content=[AssistantMessageContent(text=clean_ui_text, annotations=[])]
            )
            yield ThreadItemAddedEvent(item=assistant_item)
            yield ThreadItemDoneEvent(item=assistant_item)

            # 2. Yield a hidden context item (Internal memory with UUIDs/Tool Results)
            hidden_id = f"hidden_{item_id}"
            hidden_item = HiddenContextItem(
                id=hidden_id,
                thread_id=thread.id,
                created_at=datetime.now(),
                content=internal_memory_text
            )
            yield ThreadItemAddedEvent(item=hidden_item)
            yield ThreadItemDoneEvent(item=hidden_item)

        except Exception as e:
            # Log error
            import traceback
            traceback.print_exc()
            
            # Use specific ErrorEvent for failures
            try:
                yield ErrorEvent(message=f"An error occurred: {str(e)}")
            except:
                pass
