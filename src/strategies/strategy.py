from utils.logger import log
import asyncio
import aiohttp


class Strategy:
    async def stream_processor(self):
        raise NotImplementedError

    def __init__(self, queues, product):
        self.stop = False
        self.queues = queues
        self.product = None
        self.name = None

    async def activate(self):
        async with aiohttp.ClientSession() as self.session:
            await self.stream_processor()

    async def kill(self, product=None):
        await log('Cancelling all orders')
        self.stop = True
        await place.cancel_all(self.auth, self.session, product)

