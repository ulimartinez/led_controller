import asyncio
import websockets

async def hello(websocket, path):
    name = await websocket.recv()
    print(name)

    greeting = "Hello !"

    await websocket.send(greeting)
    print(greeting)

start_server = websockets.serve(hello, None, 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
