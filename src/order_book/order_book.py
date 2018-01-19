from src.authorization import CoinbaseExchangeAuth
from os import environ as env
from websocket import create_connection
from json import dumps, loads
from utils.logger import log
from threading import Thread
from collections import deque
import asyncio
import aiohttp
import websockets


class Trader:
    def __init__(self, products=['BTC-USD'], channels=['level2']):
        self.stop = False
        self.queue = deque()
        self.sub_message = {
            "type": "subscribe",
            "product_ids": products,
            "channels": channels
        }
        self.web_socket = create_connection(env['WEBSOCKET_URL'])
        self.web_socket.send(dumps(sub_message))
        log('Initiating connection.')
        async with aiohttp.ClientSession() as self.session:
            self.listener = Thread(target=tune_in, name='listener')
            self.reactor = Thread(target=react, name='reactor')
            self.listener.start()
            self.reactor.start()

    def tune_in(self):
        self._listen()
        self._close()

    def _listen(self):
        while not self.stop:
            try:
                if int(time.time() % 30) == 0:
                    self.web_socket.ping('keepalive')
                msg = loads(self.web_socket.recv())
                if msg['type'] == 'snapshot':
                    self.queue.clear()
                    self.queue.appendleft({ 'type': msg['type'],
                                            'bids': msg['bids'],
                                            'asks': msg['asks'] })
                else:
                    self.queue.appendleft({ 'type':msg['type'],
                                            'changes': msg['changes'] })
            except Exception as e:
                log(e, 'error')

    def _close(self):
        self.stop = True
        try:
            self.web_socket.close()
        except:
            pass
        self.listener.join()

