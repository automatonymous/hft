from json import dumps, loads
from os import environ as env
from websocket import create_connection

from src.authorization import get_auth_dict
from utils.logger import log


class Channel:
    def __init__(self, queue, products=['BTC-USD'], channels=['level2']):
        self.alive = False
        self.queue = queue
        self.sub_message = get_auth_dict()
        self.channels = channels
        self.sub_message.update({
            "type": "subscribe",
            "product_ids": products,
            "channels": self.channels,
        })

    def listen(self):
        log(f'{self.channels} --- Initializing connection')
        cycles = 0
        try:
            self.alive = True
            websocket = create_connection(env['WEBSOCKET_URL'])
            websocket.send(dumps(self.sub_message))
            while self.alive:
                data = websocket.recv()
                self.queue.push(loads(data))
                cycles += 1
                if cycles % 300 == 0:
                    websocket.ping('keepalive')
                    log(
                        f'{self.channels} --- Still alive asof {cycles}'
                    )
        except Exception as e:
            log(f'{self.channels} --- {e}', level='error')

    def stop(self):
        log(f'{self.channels} --- Destroying connection')
        self.alive = False

