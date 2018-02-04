from utils.logger import log
from src.strategies.strategy import Strategy


class PrintStuff(Strategy):
    def stream_processor(self):
        while not self.stop:
            try:
                msg = self.queue.pop()
                log(f"Reading msg {msg['type']}")
            except IndexError:
                continue

