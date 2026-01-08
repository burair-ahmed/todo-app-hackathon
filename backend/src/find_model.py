import asyncio
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from backend.src.services.agent_service import client

async def find_flash_model():
    print("--- Searching for Flash Models ---")
    try:
        models = await client.models.list()
        found = False
        for m in models.data:
            if "flash" in m.id:
                print(f"FOUND: {m.id}")
                found = True
        if not found:
            print("No 'flash' models found.")
            # validation: print first 5
            for i, m in enumerate(models.data):
                if i < 5: print(m.id)
    except Exception as e:
        print(f"Error listing models: {e}")

if __name__ == "__main__":
    asyncio.run(find_flash_model())
