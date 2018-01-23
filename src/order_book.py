from json import dumps, loads
from os import environ as env
import websockets

from src.authorization import CoinbaseExchangeAuth
from utils.logger import log


class OrderBook:
    def __init__(self, queue, products=['BTC-USD'], channels=['level2']):
        self.alive = False
        self.queue = queue
        self.sub_message = { "type": "subscribe",
                              "product_ids": products,
                              "channels": channels }

    async def listen(self):
        await log('Initializing connection')
        try:
            self.alive = True
            async with websockets.connect(env['WEBSOCKET_URL']) as websocket:
                await websocket.send(dumps(self.sub_message))
                async for message in websocket:
                    if not self.alive: break
                    self.queue.push(loads(message))
        except Exception as e:
            await log(e, level='error')

    async def stop(self):
        await log('Destroying connection')
        self.alive = False

