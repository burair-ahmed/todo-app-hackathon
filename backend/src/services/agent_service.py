import os
import json
import inspect
import traceback
from typing import List, Dict, Any, Optional
from datetime import datetime

from ..models.message import Message
from ..services.mcp_server import get_mcp_tools
from ..config import settings
from agents import Agent
from openai import AsyncOpenAI
import google.generativeai as genai

# Initialize the OpenAI Client pointing to Gemini
# Docs: https://ai.google.dev/gemini-api/docs/openai
GEMINI_API_KEY = settings.GEMINI_API_KEY
client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Get MCP tools
mcp_tools_map = get_mcp_tools()

# Define tools for the agent (OpenAI Format)
agent_tools = list(mcp_tools_map.values())

# Define the Agent using the SDK's abstraction
agent = Agent(
    name="Todo Assistant",
    instructions="You are a helpful Task Management Assistant. User ID must be passed to all tools.",
    model="models/gemini-flash-latest", 
    tools=agent_tools
)

async def run_agent(
    user_id: str,
    user_message: str,
    history: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Run the agent loop (ReAct pattern) using OpenAI-compatible Gemini client.
    Returns:
        {
            "response": str,       # Final answer to user
            "tool_trace": str      # Debug trace of tool execution
        }
    """
    TRACE = [] # Keep track of execution steps for hidden context

    try:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("agent_debug.log", "a") as log_file:
            log_file.write(f"\n\n--- [AGENT] Starting run_agent for user {user_id} at {current_time} ---\n")
            log_file.write(f"--- [AGENT] User Message: {user_message} ---\n")
        
        # 1. Prepare Initial System Prompt
        system_instruction = f"""
        {agent.instructions}
        Current User ID: {user_id}
        Current Local Time: {current_time}
        
        IMPORTANT RULES:
        - You are an agent that manages tasks for the specific User ID provided above.
        - ALWAYS pass the `user_id` argument to every tool call.
        - Using the tools is the ONLY way to change the database.
        - If the user asks to "list", "add", "complete", "delete", or "update", USE THE TOOLS.
        - Do not hallucinate task IDs. Use `list_tasks` to find IDs if you don't know them.
        """

        messages = [{"role": "system", "content": system_instruction}]
        
        # Add History
        # History is expected to be [{"role": "user"|"assistant", "content": "..."}]
        messages.extend(history)
        
        # Add User Message
        messages.append({"role": "user", "content": user_message})

        # 2. ReAct Loop
        MAX_TURNS = 5
        final_response_text = ""
        
        print(f"--- [AGENT] Entering ReAct Loop (Max Turns: {MAX_TURNS}) ---")
        with open("agent_debug.log", "a") as log_file:
            log_file.write(f"--- [AGENT] Entering ReAct Loop (Max Turns: {MAX_TURNS}) ---\n")

        for turn in range(MAX_TURNS):
            print(f"--- [AGENT] Turn {turn+1}/{MAX_TURNS} ---")
            with open("agent_debug.log", "a") as log_file:
                log_file.write(f"--- [AGENT] Turn {turn+1}/{MAX_TURNS} ---\n")
            
            # Call Model
            completion = await client.chat.completions.create(
                model=agent.model,
                messages=messages,
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
            
            message = completion.choices[0].message
            messages.append(message) # Add assistant message to history
            
            tool_calls = message.tool_calls
            
            if tool_calls:
                # Execute Tools
                TRACE.append(f"Turn {turn+1}: AI decided to call {len(tool_calls)} tools.")
                
                for tc in tool_calls:
                    func_name = tc.function.name
                    func_args_str = tc.function.arguments
                    call_id = tc.id
                    
                    TRACE.append(f"  -> Calling {func_name} with {func_args_str}")
                    
                    # Execute
                    tool_result_content = ""
                    try:
                        args = json.loads(func_args_str)
                        if func_name in mcp_tools_map:
                            func = mcp_tools_map[func_name]
                            
                            # Check awaitable
                            if inspect.iscoroutinefunction(func):
                                result = await func(**args)
                            else:
                                result = func(**args)
                                
                            tool_result_content = json.dumps(result)
                        else:
                            tool_result_content = json.dumps({"error": f"Tool {func_name} not found"})
                            
                    except Exception as e:
                        tool_result_content = json.dumps({"error": f"Execution failed: {str(e)}"})
                        TRACE.append(f"     [ERROR] {str(e)}")

                    TRACE.append(f"     Result: {tool_result_content}")

                    # Append Result Message (Role: tool)
                    messages.append({
                        "role": "tool",
                        "tool_call_id": call_id,
                        "name": func_name,
                        "content": tool_result_content
                    })

            else:
                # No tool calls -> This is the final answer
                final_response_text = message.content or ""
                TRACE.append(f"Turn {turn+1}: Final Answer Generated.")
                break
        
        if not final_response_text:
             final_response_text = "I completed the actions, but forgot to write a final summary."

        return {
            "response": final_response_text,
            "tool_trace": "\n".join(TRACE)
        }

    except Exception as e:
        import traceback
        err = traceback.format_exc()
        print(f"AGENT ERROR: {err}")
        with open("agent_debug.log", "a") as log_file:
            log_file.write(f"[CRITICAL AGENT ERROR]: {err}\n")
        return {
            "response": f"Sorry, I encountered an internal error: {str(e)}",
            "tool_trace": f"Error Log:\n{err}"
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
        param_type = "string" # Default
        if annotation in type_map:
            param_type = type_map[annotation]
        
        if "List" in str(annotation):
             param_type = "array"

        parameters["properties"][name] = {
            "type": param_type,
            "description": f"Parameter {name}"
        }
        
        if param.default == inspect.Parameter.empty:
            parameters["required"].append(name)
            
    return parameters

# Backwards compatibility dummy
async def execute_tool_call(tool_name: str, arguments: Dict[str, Any]):
    pass

def detect_tool_calls(ai, user, uid):
    return []