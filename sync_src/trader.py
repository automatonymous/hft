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
            t = Thread(target=func)
            t.start()

