import asyncio
from threading import Thread


class Trader:
    def __init__(self, channels, strat):
        self.ch = channels
        self.strat = strat
        if isinstance(self.ch, list):
            self.funx = [x.listen for x in self.ch]
        else:
            self.funx = [self.ch.listen]
        self.funx.append(
            self.strat.activate,
        )

    def run(self):
        for func in self.funx:
            t = Thread(target=self._create_loop, args=(func,))
            t.start()

    def _create_loop(self, target):
        new_loop = asyncio.new_event_loop()
        new_loop.run_until_complete(target())

