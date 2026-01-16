import asyncio
import os
from tripo3d import TripoClient
from dotenv import load_dotenv

load_dotenv()

async def main():
    api_key = os.getenv("TRIPO_API_KEY")
    client = TripoClient(api_key=api_key)
    print("Client created")
    # Just checking the type of return, not actually waiting for full generation if possible,
    # or just catching the error to confirm it works.
    try:
        # Pass a dummy prompt to see if it awaits
        task = await client.text_to_model(prompt="test prompt")
        print("Task created:", task)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    asyncio.run(main())
