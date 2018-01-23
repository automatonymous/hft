from utils.logger import log
from src.authorization import CoinbaseExchangeAuth
import asyncio
import aiohttp


class Strategy:
    async def stream_processor(self):
        raise NotImplementedError

    def __init__(self, queue):
        self.stop = False
        self.auth = CoinbaseExchangeAuth()
        self.queue = queue

    async def activate(self):
        async with aiohttp.ClientSession() as self.session:
            await self.stream_processor()


    async def kill(self, product=None):
        await log('Cancelling all orders')
        self.stop = True
        await place.cancel_all(self.auth, self.session, product)

