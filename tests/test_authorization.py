import pytest
import requests
from os import environ as env
from src.authorization import CoinbaseExchangeAuth


def test_CoinbaseExchangeAuth():
    url = env['GDAX_URL']+'position'
    auth = CoinbaseExchangeAuth()
    response = requests.get(url, auth=auth)
    assert response.status_code == 200
    assert response.json()['status'] == 'active'

