import os
import asyncio
import websockets

async def client():
    server_ip = os.getenv("SERVER_IP", "127.0.0.1")
    uri = f"ws://{server_ip}:8765"
    
    async with websockets.connect(uri) as websocket:
        print(f"Connected to server at {uri}!")
        try:
            while True:
                message = input("Enter message to send to server (or 'quit' to exit): ")
                if message.lower() == 'quit':
                    break
                
                await websocket.send(message)
                response = await websocket.recv()
                print(f"Received from server: {response}")
        except websockets.exceptions.ConnectionClosed:
            print("Connection closed")

if __name__ == "__main__":
    asyncio.run(client())
