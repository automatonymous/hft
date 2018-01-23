import asyncio
from threading import Thread


class Trader:
    def __init__(self, q, book, strat):
        self.q = q
        self.ob = book
        self.strat = strat
        self.funx = (
            self.ob.listen,
            self.strat.activate,
        )

    def run(self):
        for func in self.funx:
            t = Thread(target=self._create_loop, args=(func,))
            t.start()

    def _create_loop(self, target):
        new_loop = asyncio.new_event_loop()
        new_loop.run_until_complete(target())

