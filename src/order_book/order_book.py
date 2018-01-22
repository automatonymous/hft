from json import dumps, loads
from os import environ as env
import websockets

from src.authorization import CoinbaseExchangeAuth
from utils.logger import log


class OrderBook:
    def __init__(self, queue, products=['BTC-USD'], channels=['level2']):
        self.stop = False
        self.queue = queue
        self.sub_message = { "type": "subscribe",
                              "product_ids": products,
                              "channels": channels }

    async def listen(self):
        log('Initializing connection')
        try:
            async with websockets.connect(env['WEBSOCKET_URL']) as websocket:
                await websocket.send(dumps(self.sub_message))
                async for message in websocket:
                    if self.stop: break
                    await self.queue.push(message)
        except Exception as e:
            log(e, level='error')

    async def stop(self):
        log('Destroying connection')
        self.stop = True

