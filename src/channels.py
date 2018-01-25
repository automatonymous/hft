from json import dumps, loads
from os import environ as env
import websockets

from src.authorization import get_auth_dict
from utils.logger import log


class Channel:
    def __init__(self, queue, products=['BTC-USD'], channels=['level2']):
        self.alive = False
        self.queue = queue
        self.sub_message = get_auth_dict()
        self.channels = channels
        self.sub_message.update({
            "type": "subscribe",
            "product_ids": products,
            "channels": self.channels,
        })

    async def listen(self):
        await log(f'{self.channels} --- Initializing connection')
        cycles = 0
        try:
            self.alive = True
            async with websockets.connect(
                env['WEBSOCKET_URL'],
                max_queue=0,
            ) as websocket:
                await websocket.send(dumps(self.sub_message))
                async for message in websocket:
                    if not self.alive: break
                    await self.queue.push(loads(message))
                    cycles += 1
                    if cycles % 30 == 0:
                        websocket.ping('keepalive')
                        await log(
                            f'{self.channels} --- Still alive asof {cycles}'
                        )
        except Exception as e:
            await log(f'{self.channels} --- {e}', level='error')

    async def stop(self):
        await log(f'{self.channels} --- Destroying connection')
        self.alive = False


if __name__ == '__main__':
    from src.data_structures import L2Queue
    import asyncio

    q = L2Queue()
    x = Channel(q)
    n = asyncio.new_event_loop()
    n.run_until_complete(x.listen())

