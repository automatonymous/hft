from src.data_structures import TickerQueue, UserMatchQueue
from src.channels import Channel
from src.strategies.trailing_stop import TrailingStop
from src.trader import Trader


def trailing_stop(product):
    q = TickerQueue()
    ch = Channel(q, products=[product], channels=['ticker'])
    strat = TrailingStop(q, product)
    trader = Trader(ch, strat)
    trader.run()

if __name__ == '__main__':
    trailing_stop('BTC-USD')

