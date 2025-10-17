import os
import asyncio
import websockets
import json
import pyaudio
from dotenv import load_dotenv
from vosk import Model, KaldiRecognizer

load_dotenv()

# Audio configuration
RATE = 16000
CHUNK = 4096

async def client():
    server_ip = os.getenv("SERVER_IP", "127.0.0.1")
    uri = f"ws://{server_ip}:8765"
    
    # Initialize Vosk model
    model_path = os.getenv("VOSK_MODEL_PATH", "model")
    
    if not os.path.exists(model_path):
        print(f"Error: Vosk model not found at '{model_path}'")
        return
    
    print(f"Loading Vosk model from {model_path}...")
    model = Model(model_path)
    recognizer = KaldiRecognizer(model, RATE)
    recognizer.SetWords(True)
    
    # Initialize PyAudio
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK
    )
    stream.start_stream()
    
    print("Microphone initialized!")
    
    async with websockets.connect(uri) as websocket:
        print(f"Connected to server at {uri}!")
        print("Listening for audio... Press Ctrl+C to stop.\n")
        
        try:
            while True:
                # Read audio data
                loop = asyncio.get_event_loop()
                data = await loop.run_in_executor(None, stream.read, CHUNK, False)
                
                # Process with Vosk
                if recognizer.AcceptWaveform(data):
                    # Final result (end of speech)
                    result = json.loads(recognizer.Result())
                    text = result.get('text', '').strip()
                    
                    if text:
                        print(f"[Transcribed]: {text}")
                        await websocket.send(text)
                        
                        # Wait for response from server
                        try:
                            response = await asyncio.wait_for(
                                websocket.recv(), 
                                timeout=5.0
                            )
                            print(f"[Server]: {response}\n")
                        except asyncio.TimeoutError:
                            print("[Server]: No response (timeout)\n")
                else:
                    # Partial result (still speaking)
                    partial = json.loads(recognizer.PartialResult())
                    partial_text = partial.get('partial', '')
                    if partial_text:
                        print(f"[Listening]: {partial_text}", end='\r')
                        
        except websockets.exceptions.ConnectionClosed:
            print("\nConnection closed")
        except KeyboardInterrupt:
            print("\nStopping...")
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()

if __name__ == "__main__":
    asyncio.run(client())
