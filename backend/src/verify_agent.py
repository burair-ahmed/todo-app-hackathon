import asyncio
import os
import sys
from typing import List

# Adjust path to find modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.src.services.agent_service import process_chat_request
from backend.src.models.message import Message
try:
    from backend.src.models.user import User
except ImportError:
    pass # If User model doesn't exist or is named differently, we skip. But it likely exists.

async def test_agent():
    user_id = "test-user-123"
    
    # Debug: List models
    from backend.src.services.agent_service import client
    print("--- Listing Available Models ---")
    try:
        models = await client.models.list()
        for m in models.data:
            print(f"Model: {m.id}")
    except Exception as e:
        print(f"Error listing models: {e}")

    print("--- Test 1: Add Task ---")
    user_message = "Add a task called 'Buy groceries' due tomorrow"
    history = []
    
    print(f"User: {user_message}")
    result = await process_chat_request(user_id, 1, user_message, history)
    
    print("Agent Response:", result["response"])
    print("Tool Calls:", result["tool_calls"])
    
    if result["tool_calls"]:
        print("✅ Tool call detected!")
        # check if name is add_task
        if result["tool_calls"][0]["name"] == "add_task":
             print("✅ Correct tool selected: add_task")
        else:
             print(f"❌ Wrong tool: {result['tool_calls'][0]['name']}")
    else:
        print("❌ No tool call detected.")

    print("\n--- Test 2: List Tasks ---")
    user_message = "What tasks do I have?"
    history.append(Message(role="user", content="Add a task called 'Buy groceries' due tomorrow"))
    history.append(Message(role="assistant", content="I've added the task.")) 
    
    print(f"User: {user_message}")
    result = await process_chat_request(user_id, 1, user_message, history)
    
    print("Agent Response:", result["response"])
    print("Tool Calls:", result["tool_calls"])
    
    if result["tool_calls"]:
        if result["tool_calls"][0]["name"] == "list_tasks":
             print("✅ Correct tool selected: list_tasks")
        else:
             print(f"❌ Wrong tool: {result['tool_calls'][0]['name']}")
    else:
        print("❌ No tool call detected.")

if __name__ == "__main__":
    asyncio.run(test_agent())
