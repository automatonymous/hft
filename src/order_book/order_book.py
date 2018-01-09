from src.authorization import CoinbaseExchangeAuth
from os import environ as env
import requests


class OrderBook:
    def __init__(self, product):
