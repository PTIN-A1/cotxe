import asyncio
import websockets


async def echo(websocket, path):
    print("Client connected", flush=True)
    async for message in websocket:
        print(f"Received and echoing message: {message}", flush=True)
        await websocket.send(message)


start_server = websockets.serve(echo, "127.0.0.1", 8000)

print("WebSockets echo server starting", flush=True)
asyncio.get_event_loop().run_until_complete(start_server)

print("WebSockets echo server running", flush=True)
asyncio.get_event_loop().run_forever()
