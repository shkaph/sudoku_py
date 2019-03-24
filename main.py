#!/usr/bin/env python3

import sys
import asyncio
import websockets

async def hello(websocket, path):
    name = await websocket.recv()
    print(f"< {name}")

    greeting = f"Hello {name}!"

    await websocket.send(greeting)
    print(f"> {greeting}")

start_server = websockets.serve(hello, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

'''

def main():
	print ('Python 3.x.x must be installed')
	argv = sys.argv
	argc = len(argv)
	print (argc, argv)

if __name__ == '__main__':
	main()'''