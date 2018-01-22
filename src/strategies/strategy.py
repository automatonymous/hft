from utils.logger import log
from src.actions import orders as place
import asyncio
import aiohttp


class Strategy:
    async def stream_processor(self):
        raise NotImplementedError

    def __init__(self, auth, queue):
        self.stop = False
        self.auth = auth
        self.queue = queue
        async with aiohttp.ClientSession() as self.session:
            await self.stream_processor(queue)

    async def kill(self, product=None):
        await log('Cancelling all orders')
        await self.stop = True
        await place.cancel_all(self.auth, self.session, product)

