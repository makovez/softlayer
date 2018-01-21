# test_client.py
import asyncio
import time

import websockets


async def client(client_id, n):
    t0 = time.time()
    async with websockets.connect('ws://104.238.158.53:4041/') as websocket:
        print("[#{}] > {}".format(client_id, n))
        await websocket.send(str(n))
        while True:
            resp = await websocket.recv()
            print("[#{}]".format(client_id))

    print("[#{}] Done in {:.2f} seconds".format(client_id, time.time() - t0))


tasks = [client(i + 1, 3) for i in range(500)]
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))
loop.close()