import asyncio
import websockets
import json
async def hello():
    uri = "ws://localhost:8000/ws/fetchTweet/add/"
    async with websockets.connect(uri) as websocket:
        while True:
            name = input("What's your name? ")
            await websocket.send(name)
            print(f"> {name}")

            greeting = await websocket.recv()
            print(f"< {greeting}")

asyncio.get_event_loop().run_until_complete(hello())