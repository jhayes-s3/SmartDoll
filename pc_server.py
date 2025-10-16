import asyncio
import websockets

async def handle_client(websocket):
    print("Client connected!")
    try:
        async for message in websocket:
            print(f"Received from client: {message}")
            
            # Send response back to client
            response = input("Enter message to send to client: ")
            await websocket.send(response)
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")

async def main():
    async with websockets.serve(handle_client, "0.0.0.0", 8765):
        print("WebSocket server started on ws://0.0.0.0:8765")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())