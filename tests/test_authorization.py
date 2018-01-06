import pytest
import requests
from authorization import CoinbaseExchangeAuth


def test_CoinbaseExchangeAuth():
    url = 'https://api.gdax.com/currencies'
    auth = CoinbaseExchangeAuth()
    response = requests.get(url, auth=auth)
    assert response.status_code == 200

