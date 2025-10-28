import asyncio
import websockets
from openai import AsyncOpenAI

# Initialize the client to point to LM Studio
client = AsyncOpenAI(
    base_url="http://localhost:1234/v1",
    api_key="not-needed" 
)




async def handle_client(websocket):
    print("Client connected!")
    try:
        async for message in websocket:
            print(f"Received from client: {message}")

            response = await client.responses.create(
            model="llama-3.2-3b-instruct",
            input= message
            )
            print(f"LLM Response: {response.output[0].content[0].text}")
            await websocket.send(response.output[0].content[0].text)

    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")

async def main():
    async with websockets.serve(handle_client, "0.0.0.0", 8765):
        print("WebSocket server started on ws://0.0.0.0:8765")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())