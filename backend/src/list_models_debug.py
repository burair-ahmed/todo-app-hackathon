import asyncio
import os
import sys

# Adjust path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# Mock environment if needed or just use logic
from backend.src.services.agent_service import client

async def list_models():
    print("--- Listing Available Models ---")
    try:
        models = await client.models.list()
        for m in models.data:
            print(f"Model: {m.id}")
    except Exception as e:
        print(f"Error listing models: {e}")

if __name__ == "__main__":
    asyncio.run(list_models())
