from collections import deque
from utils.logger import log
import asyncio


class L2Queue(deque):
    async def push(self, msg):
        if msg['type'] == 'snapshot':
            self.clear()
            self.appendleft({
                'type': msg['type'],
                'bids': msg['bids'],
                'asks': msg['asks']
            })
        elif msg['type'] in ('subscriptions', 'error'):
            await log(msg)
        else:
            self.appendleft({
                'type': msg['type'],
                'product_id': msg['product_id'],
                'changes': msg['changes']
            })


class TickerQueue(deque):
    async def push(self, msg):
        if msg['type'] in ('subscriptions', 'error'):
            await log(msg)
        else:
            self.appendleft(msg)


class UserMatchQueue(deque):
    async def push(self, msg):
        if msg['type'] == 'match':
            self.appendleft(msg)
        else:
            await log(msg)

