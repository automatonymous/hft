from src.data_structures import MsgQueue
from src.order_book.order_book import OrderBook
from src.strategies.print_stuff import PrintStuff
from src.trader import Trader


def trade():
    q = MsgQueue()
    ob = OrderBook(q, products=['BTC-USD'], channels=['level2'])
    strat = PrintStuff(q)
    trader = Trader(q, ob, strat)
    trader.run()

if __name__ == '__main__':
    trade()

