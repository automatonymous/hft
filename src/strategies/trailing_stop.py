from utils.logger import log
import asyncio
import aiohttp

from src.strategies import Strategy


class TrailingStop(Strategy):
    async def stream_processor(self):
        #TODO implement this strategy
        async while not self.stop:
            try:
                msg = self.queue.pop()
            except IndexError:
                await log('No message to process.')
                continue

