import pytest
import requests
from src.authorization import CoinbaseExchangeAuth


def test_CoinbaseExchangeAuth():
    url = 'https://api.gdax.com/position'
    auth = CoinbaseExchangeAuth()
    response = requests.get(url, auth=auth)
    assert response.status_code == 200
    assert response.json()['status'] == 'active'

