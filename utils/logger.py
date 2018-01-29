import logging
import asyncio
from datetime import date, datetime

logging.basicConfig(
    format='%(asctime)s --- %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    level=logging.INFO
)

async def log(msg, level='info'):
    with open(f'log_file_{date.today()}.txt', 'a') as log_file:
        log_file.write(
            f'{datetime.now()} --- {msg}\n')
    getattr(logging, level)(msg)

