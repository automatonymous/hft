from utils.logger import log
import asyncio
import aiohttp

from src.strategies.strategy import Strategy


class PrintStuff(Strategy):
    async def stream_processor(self):
        while not self.stop:
            try:
                msg = self.queue.pop()
                await log(f"Reading msg {msg['type']}")
            except IndexError:
                continue
            print(msg['type'])

