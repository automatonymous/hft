from src.strategies.strategy import Strategy
from src.actions import orders as place
from utils.logger import log
from utils import gets
from collections import deque
from datetime import datetime as dt


class TrailingStop(Strategy):
    """
    This strategy requires a ticker stream and user stream.
    The idea of this strategy is to set moving stop-loss orders in order
    to lock in gains.
    """
    def stream_processor(self):
        self.name = 'Trailing Stop'
        last_tick = 0
        self.slope = 0
        self.q = self.queues
        self.hodling = False
        self.funds = gets.get_position
        self.last_30 = deque(maxlen=30)
        log(f"{self.name} --- {self.funds('USD')}")
        try:
            while not self.stop:
                try: msg = self.q.pop()
                except IndexError: continue
                if msg['sequence'] <= last_tick: continue
                else:
                    last_tick = int(msg['sequence'])
                    self.current_price = float(msg['price'])
                    self.last_30.appendleft(msg)
                if len(self.last_30) < 30:
                    log(f"{self.name} --- Filling queue")
                    continue
                time_0 = self.last_30.pop()
                t0_p = time_0['price']
                t0_t = time_0.get('time')
                if t0_t:
                    self.slope = (
                        ( float(t0_p) - float(msg['price']) ) /
                        (
                            # 2017-09-02T17:05:49.250000Z
                            dt.strptime(t0_t, '%Y-%m-%dT%H:%M:%S.%fZ') -
                            dt.strptime(msg['time'], '%Y-%m-%dT%H:%M:%S.%fZ')
                        ).total_seconds()
                    )
                if not self.hodling:
                    log(f"{self.name} --- Slope -- {self.slope}")
                    if 0.10 <= self.slope:
                        self.enter_market()
                else:
                    if any(
                        self.stop_loss[1]['id'] not in opens,
                        self.trailer[1]['id'] not in opens,
                    ):
                        self.hodling = False
                        log(f"{self.name} -- stops were filled")
                        continue
                    log(f"{self.name} --- Updating orders")
                    self.update_trailer()
                    opens = place.list_orders(
                        self.session, self.product
                    )
                    if any(
                        self.stop_loss[1]['id'] not in opens,
                        self.trailer[1]['id'] not in opens,
                    ):
                        self.hodling = False
        except KeyError as e:
            log(f'{self.name} --- Error --- {e}', level='error')
            log(f'{self.name} --- msg --- {msg}', level='error')
            log(f'{self.name} --- time_0 --- {time_0}', level='error')
        except Exception as e:
            log(f'{self.name} --- Error --- {e}', level='error')

    def enter_market(self):
        log(f"{self.name} --- Entering market at {self.current_price}")
        order = place.market_order(
            self.session, 'buy', self.product, self.funds('USD'), 'funds'
        )
        self.hodling = True
        log(f'{self.name} --- {order[0] : order[1]}')
        self.stop_loss = place.stop_order(
            self.session, 'sell',
            self.product, round(self.current_price * 0.97, 2),
            self.funds('BTC'), 'size'
        )
        log(f'{self.name} --- {self.stop_loss[0] : self.stop_loss[1]}')
        self.trailer = place.stop_order(
            self.session, 'sell',
            self.product, round(self.current_price * 0.975, 2),
            self.funds('BTC'), 'size'
        )
        log(f'{self.name} --- {self.trailer[0] : self.trailer[1]}')

    def update_trailer(self):
        cancelled = None
        while cancelled != 200:
            cancelled = place.cancel_order(
                self.session, self.trailer[1]['id']
            )
        log(f"{self.name} --- Cancelled -- {self.trailer[1]['id']}")
        self.trailer = None
        self.trailer = place.stop_order(
            self.session, 'sell',
            self.product, self.get_window(),
            self.funds('BTC'), 'size'
        )
        log(f'{self.name} --- Updated --- {self.trailer}')

    def get_window(self):
        return round( self.current_price * ( 0.975 - (self.slope * .01) ), 2 )

