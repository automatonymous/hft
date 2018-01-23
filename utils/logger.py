import logging
import asyncio

logging.basicConfig(
    format='%(asctime)s --- %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    level=logging.INFO
)
# TODO ensure logging is actually asynchronous
async def log(msg, level='info'):
    getattr(logging, level)(msg)

