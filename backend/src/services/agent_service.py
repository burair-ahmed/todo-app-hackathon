import os
import json
import inspect
from typing import List, Dict, Any
from ..models.message import Message
from ..services.mcp_server import get_mcp_tools
from ..config import settings
from agents import Agent
from openai import AsyncOpenAI

# Initialize the OpenAI Client pointing to Gemini
# Docs: https://ai.google.dev/gemini-api/docs/openai
GEMINI_API_KEY = settings.GEMINI_API_KEY
client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Get MCP tools
mcp_tools_map = get_mcp_tools()

# Define tools for the agent
agent_tools = list(mcp_tools_map.values())

# Define the Agent using the SDK's abstraction
# We use this to organize the agent's definition (instructions, model, tools)
agent = Agent(
    name="Todo Assistant",
    instructions="You are a helpful Task Management Assistant. User ID must be passed to tools contextually.",
    model="models/gemini-flash-latest", 
    tools=agent_tools
)

async def process_chat_request(
    user_id: str,
    conversation_id: int,
    user_message: str,
    conversation_history: List[Message]
) -> Dict[str, Any]:
    """
    Process a chat request using the OpenAI Agents SDK (backed by Gemini).
    """
    try:
        # 1. Prepare history
        messages = []
        for msg in conversation_history:
            messages.append({"role": msg.role, "content": msg.content})
        
        messages.append({"role": "user", "content": user_message})

        # 2. Prepare System Prompt with Context
        instructions_with_context = f"""
        {agent.instructions}
        Current User ID: {user_id}
        ALWAYS pass this User ID to any tool you call.
        """
        
        # 3. Call the model using the OpenAI Client compatibility layer
        # We manually drive the "Agent" here to ensure strict control over the client (Gemini URL)
        # and stateless behavior required by the architecture.
        
        response = await client.chat.completions.create(
            model=agent.model,
            messages=[
                {"role": "system", "content": instructions_with_context},
                *messages
            ],
            tools=[{
                "type": "function",
                "function": {
                    "name": tool.__name__,
                    "description": tool.__doc__ or "",
                    "parameters": tool.json_schema() if hasattr(tool, "json_schema") else _infer_schema(tool)
                }
            } for tool in agent.tools],
            tool_choice="auto"
        )
        
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls
        
        # 4. Format Tool Calls for the API
        formatted_tool_calls = []
        if tool_calls:
            for tc in tool_calls:
                formatted_tool_calls.append({
                    "name": tc.function.name,
                    "arguments": json.loads(tc.function.arguments)
                })
        
        return {
            "response": response_message.content or "", 
            "tool_calls": formatted_tool_calls
        }

    except Exception as e:
        import traceback
        print(f"AGENT ERROR: {traceback.format_exc()}")
        return {
            "response": f"Sorry, I encountered an error: {str(e)}",
            "tool_calls": []
        }

def _infer_schema(func):
    """
    Infer OpenAI-compatible JSON schema from function signature.
    """
    sig = inspect.signature(func)
    parameters = {
        "type": "object",
        "properties": {},
        "required": [],
        "additionalProperties": False 
    }
    
    type_map = {
        str: "string",
        int: "integer",
        bool: "boolean",
        float: "number",
        type(None): "null"
    }

    for name, param in sig.parameters.items():
        annotation = param.annotation
        # Handle basic types and Optional
        param_type = "string" # Default
        if annotation in type_map:
            param_type = type_map[annotation]
        
        # Simple list handling if annotation is straight forward (e.g. List[str])
        # This is a basic inference meant for the known MCP tools which use simple types.
        if "List" in str(annotation):
             param_type = "array"

        parameters["properties"][name] = {
            "type": param_type,
            "description": f"Parameter {name}"
        }
        
        if param.default == inspect.Parameter.empty:
            parameters["required"].append(name)
            
    return parameters

def initialize_agent():
    """
    Dummy initialization function for backward compatibility.
    """
    pass

# --- Compatibility Layer for ChatKit and Legacy APIs ---
# These functions are used by chatkit_service.py and chat_api.py
# ensuring the rest of the application continues to function while we migrate.

import re

async def execute_tool_call(tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute a tool call with the given arguments.
    Used by chat_api.py and chatkit_service.py.
    """
    if tool_name in mcp_tools_map:
        tool_func = mcp_tools_map[tool_name]
        try:
            # Check if arguments is a string (JSON) or dict
            if isinstance(arguments, str):
                try:
                    arguments = json.loads(arguments)
                except:
                    pass
            
            # Use inspect to check if we need to await
            import asyncio
            result = tool_func(**arguments)
            
            if inspect.iscoroutine(result):
                return await result
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

def detect_tool_calls(ai_response: str, user_message: str, user_id: str) -> List[Dict[str, Any]]:
    """
    Detect if any tool calls should be made based on the user's request and AI response.
    Legacy/Fallback logic used by ChatKit Service.
    """
    tool_calls = []

    # 1. Try parsing structured JSON from AI response [JSON: ...]
    json_blocks = re.findall(r"\[JSON:\s*(\{.*?\})\]", ai_response, re.DOTALL)
    for block in json_blocks:
        try:
            tool_call = json.loads(block)
            if "name" in tool_call and "arguments" in tool_call:
                # Ensure user_id is correct even if AI messed it up
                # We trust the caller provided user_id
                if isinstance(tool_call["arguments"], dict):
                    tool_call["arguments"]["user_id"] = user_id
                tool_calls.append(tool_call)
        except:
            pass
    
    if tool_calls:
        return tool_calls

    # 2. Fallback to keyword matching in user message (Legacy)
    user_message_lower = user_message.lower()

    # Add task
    if any(keyword in user_message_lower for keyword in ["add task", "create task", "new task", "add a task"]):
        # Extract task title
        title_match = re.search(r"(?:to|that|for|task)\s+(.+?)(?:\s+to|$)", user_message_lower)
        if title_match:
            title = title_match.group(1).strip()
            tool_calls.append({
                "name": "add_task",
                "arguments": {
                    "user_id": user_id,
                    "title": title
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
        # Extract task ID
        id_match = re.search(r"\b(\d+)\b", user_message)
        task_id = int(id_match.group(1)) if id_match else 1
        tool_calls.append({
            "name": "complete_task",
            "arguments": {
                "user_id": user_id,
                "task_id": task_id
            }
        })

    # Update task
    elif any(keyword in user_message_lower for keyword in ["update task", "edit task", "change task"]):
        # Extract task ID
        id_match = re.search(r"\b(\d+)\b", user_message)
        task_id = int(id_match.group(1)) if id_match else 1
        
        # Simple extraction
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
        # Extract task ID
        id_match = re.search(r"\b(\d+)\b", user_message)
        task_id = int(id_match.group(1)) if id_match else 1
        tool_calls.append({
            "name": "delete_task",
            "arguments": {
                "user_id": user_id,
                "task_id": task_id
            }
        })

    return tool_calls