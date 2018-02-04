from sync_src.data_structures import TickerQueue, UserMatchQueue
from sync_src.channels import Channel
from sync_src.strategies.trailing_stop import TrailingStop
from sync_src.trader import Trader


def trailing_stop(product):
    q = TickerQueue()
    ch = Channel(q, products=[product], channels=['ticker'])
    strat = TrailingStop(q, product)
    trader = Trader(ch, strat)
    trader.run()

if __name__ == '__main__':
    trailing_stop('BTC-USD')

