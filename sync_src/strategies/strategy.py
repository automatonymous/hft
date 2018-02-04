from sync_src.utils.logger import log


class Strategy:
    def stream_processor(self):
        raise NotImplementedError

    def __init__(self, queues, product):
        self.stop = False
        self.queues = queues
        self.product = None
        self.name = None

    def activate(self):
        self.stream_processor()

    def kill(self, product=None):
        log('Cancelling all orders')
        self.stop = True
        place.cancel_all(self.auth, self.session, product)

