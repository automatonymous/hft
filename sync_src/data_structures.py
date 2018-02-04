from collections import deque
from sync_src.utils.logger import log


class L2Queue(deque):
    def push(self, msg):
        if msg['type'] == 'snapshot':
            self.clear()
            self.appendleft({
                'type': msg['type'],
                'bids': msg['bids'],
                'asks': msg['asks']
            })
        elif msg['type'] in ('subscriptions', 'error'):
            log(msg)
        else:
            self.appendleft({
                'type': msg['type'],
                'product_id': msg['product_id'],
                'changes': msg['changes']
            })


class TickerQueue(deque):
    def push(self, msg):
        if msg['type'] in ('subscriptions', 'error'):
            log(msg)
        else:
            self.appendleft(msg)


class UserMatchQueue(deque):
    def push(self, msg):
        if msg['type'] == 'match':
            self.appendleft(msg)
        else:
            log(msg)

