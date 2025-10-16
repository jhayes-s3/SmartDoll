import asyncio
import websockets

async def client():
    uri = "ws://169.254.123.187:8765"  # Replace SERVER_IP with Windows PC's IP
    async with websockets.connect(uri) as websocket:
        print("Connected to server!")
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