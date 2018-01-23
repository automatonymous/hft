from collections import deque


class MsgQueue(deque):
    def push(self, msg):
        if msg['type'] == 'snapshot':
            self.clear()
            self.appendleft({ 'type': msg['type'],
                              'bids': msg['bids'],
                              'asks': msg['asks'] })
        elif msg['type'] in ('subscriptions', 'error'):
            pass
        else:
            self.appendleft({ 'type': msg['type'],
                              'product_id': msg['product_id'],
                              'changes': msg['changes'] })

