from collections import deque


class MsgQueue(deque):
    def push(self, msg):
        if msg['type'] == 'snapshot':
            self.clear()
            self.appendleft({ 'type': msg['type'],
                              'bids': msg['bids'],
                              'asks': msg['asks'] })
        else:
            self.appendleft({ 'type': msg['type'],
                              'changes': msg['changes'] })

