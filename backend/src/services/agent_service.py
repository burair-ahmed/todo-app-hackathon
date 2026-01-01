import os
import json
import re
from typing import List, Dict, Any
from ..models.message import Message
import google.generativeai as genai
from .mcp_server import get_mcp_tools

# Initialize the Gemini client
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel('gemini-pro')

# Get MCP tools
mcp_tools = get_mcp_tools()

async def process_chat_request(
    user_id: str,
    conversation_id: int,
    user_message: str,
    conversation_history: List[Message]
) -> Dict[str, Any]:
    """
    Process a chat request using the AI agent and return the response with tool calls.
    """
    try:
        # Prepare conversation history for the AI model
        history_for_ai = []
        for msg in conversation_history:
            role = "user" if msg.role == "user" else "model"  # Gemini uses "model" instead of "assistant"
            history_for_ai.append({
                "role": role,
                "parts": [msg.content]
            })

        # Prepare the user's current message with instructions for tool usage
        user_input = f"""
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

        # Create a chat completion with the conversation history
        chat = gemini_model.start_chat(history=history_for_ai)
        response = chat.send_message(user_input)

        # Extract the AI's response
        ai_response = response.text

        # Detect if any tool calls should be made based on the AI's response
        tool_calls = detect_tool_calls(ai_response, user_message, user_id)

        return {
            "response": ai_response,
            "tool_calls": tool_calls
        }
    except Exception as e:
        # Handle any errors gracefully
        return {
            "response": f"Sorry, I encountered an error: {str(e)}",
            "tool_calls": []
        }

def detect_tool_calls(ai_response: str, user_message: str, user_id: str) -> List[Dict[str, Any]]:
    """
    Detect if any tool calls should be made based on the user's request and AI response.
    This is a simplified approach - in a real implementation, this would be more sophisticated.
    """
    tool_calls = []

    # Look for task management keywords in the user message
    user_message_lower = user_message.lower()

    # Add task
    if any(keyword in user_message_lower for keyword in ["add task", "create task", "new task", "add a task"]):
        # Extract task title and description using simple regex
        title_match = re.search(r"(?:to|that|for)\s+(.+?)(?:\s+to|$)", user_message_lower)
        if title_match:
            title = title_match.group(1).strip()
            tool_calls.append({
                "name": "add_task",
                "arguments": {
                    "user_id": user_id,
                    "title": title,
                    "description": ""
                }
            })

    # List tasks
    elif any(keyword in user_message_lower for keyword in ["list tasks", "show tasks", "my tasks", "all tasks"]):
        tool_calls.append({
            "name": "list_tasks",
            "arguments": {
                "user_id": user_id,
                "status": None
            }
        })

    # Complete task
    elif any(keyword in user_message_lower for keyword in ["complete task", "finish task", "done task", "mark as complete"]):
        # Extract task ID if mentioned
        id_match = re.search(r"\b(\d+)\b", user_message)
        task_id = int(id_match.group(1)) if id_match else 1  # Default to 1 if not specified
        tool_calls.append({
            "name": "complete_task",
            "arguments": {
                "user_id": user_id,
                "task_id": task_id
            }
        })

    # Update task
    elif any(keyword in user_message_lower for keyword in ["update task", "edit task", "change task"]):
        # Extract task ID and new information
        id_match = re.search(r"\b(\d+)\b", user_message)
        task_id = int(id_match.group(1)) if id_match else 1  # Default to 1 if not specified

        # Simple extraction of new title/description
        title_match = re.search(r"(?:to|as)\s+(.+?)(?:\.|$)", user_message_lower)
        new_title = title_match.group(1).strip() if title_match else ""

        tool_calls.append({
            "name": "update_task",
            "arguments": {
                "user_id": user_id,
                "task_id": task_id,
                "title": new_title if new_title else None
            }
        })

    # Delete task
    elif any(keyword in user_message_lower for keyword in ["delete task", "remove task"]):
        # Extract task ID if mentioned
        id_match = re.search(r"\b(\d+)\b", user_message)
        task_id = int(id_match.group(1)) if id_match else 1  # Default to 1 if not specified
        tool_calls.append({
            "name": "delete_task",
            "arguments": {
                "user_id": user_id,
                "task_id": task_id
            }
        })

    return tool_calls

def execute_tool_call(tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute a tool call with the given arguments
    """
    if tool_name in mcp_tools:
        tool_func = mcp_tools[tool_name]
        try:
            # Call the tool function with the provided arguments
            result = tool_func(**arguments)
            return result
        except Exception as e:
            return {
                "status": "error",
                "message": f"Tool execution failed: {str(e)}"
            }
    else:
        return {
            "status": "error",
            "message": f"Unknown tool: {tool_name}"
        }

def initialize_agent():
    """
    Initialize the agent with the MCP tools
    """
    # In a real implementation, this would connect the AI agent to the MCP tools
    pass

# Initialize the agent when the service is loaded
initialize_agent()