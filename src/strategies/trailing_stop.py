from src.strategies.strategy import Strategy
from src.actions import orders as place
from utils.logger import log
from utils import gets
from collections import deque
from datetime import datetime as dt
import asyncio
import aiohttp


class TrailingStop(Strategy):
    """
    This strategy requires a ticker stream and user stream.
    The idea of this strategy is to set moving stop-loss orders in order
    to lock in gains.
    """
    async def stream_processor(self):
        self.name = 'Trailing Stop'
        last_tick = 0
        self.q = self.queues
        self.hodling = False
        self.funds = gets.get_position
        self.last_30 = deque(maxlen=30)
        await log(f"{self.name} --- {self.funds('USD')}")
        try:
            while not self.stop:
                try: msg = self.q.pop()
                except IndexError: continue
                if msg['sequence'] <= last_tick: continue
                else:
                    last_tick = int(msg['sequence'])
                    self.current_price = float(msg['price'])
                    self.last_30.appendleft(msg)
                if len(self.last_30) < 30: continue
                await log(f"{self.name} --- Queue filled!")
                time_0 = self.last_30.pop()
                self.slope = (
                    ( float(time_0['price']) - float(msg['price']) ) /
                    ( dt(time_0['time']) - dt(msg['time']) ).total_seconds()
                )
                if not hodling:
                    await log(f"{self.name} --- Not hodling!")
                    if 0.58 <= self.slope <= 1.67:
                        await log(
                            f"{self.name} --- Entering market at {self.current_price}"
                        )
                        self.enter_market()
                else:
                    await log(f"{self.name} --- Updating order")
                    self.update_trailer()
                    opens = await place.list_orders(
                        self.auth, self.session, self.product
                    )
                    if any(
                        self.stop_loss[1]['id'] not in opens,
                        self.trailer[1]['id'] not in opens,
                    ):
                        hodling = False
        except KeyError as e:
            await log(f'{self.name} --- {msg}')

    async def enter_market(self):
        order = place.market_order(
            self.auth, self.session, 'buy',
            self.product, self.funds('USD'), 'funds'
        )
        self.hodling = True
        await log(f'{self.name} --- {order}')
        self.stop_loss = await place.stop_order(
            self.auth, self.session, 'sell',
            self.product, round(self.current_price * 0.97, 2),
            self.funds('BTC'), 'size'
        )
        await log(f'{self.name} --- {self.stop_loss}')
        self.trailer = await place.stop_order(
            self.auth, self.session, 'sell',
            self.product, round(self.current_price * 0.975, 2),
            self.funds('BTC'), 'size'
        )
        await log(f'{self.name} --- {self.trailer}')

    async def update_trailer(self):
        cancelled = None
        while cancelled != 200:
            cancelled = await place.cancel_order(
                self.auth, self.session, self.trailer[1]['id']
            )
        await log(f"{self.name} --- Cancelled -- {self.trailer[1]['id']}")
        self.trailer = None
        self.trailer = await place.stop_order(
            self.auth, self.session, 'sell',
            self.product, self.get_window(),
            self.funds('BTC'), 'size'
        )
        await log(f'{self.name} --- Updated --- {self.trailer}')

    def get_window(self):
        return round( self.current_price * ( 0.975 - (self.slope * .01) ), 2 )

