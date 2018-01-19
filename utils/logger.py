import logging


def log(msg, level='info'):
    logging.basicConfig(
        format='%(asctime)s --- %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p',
        level=logging.INFO
    )
    getattr(logging, level)(msg)

