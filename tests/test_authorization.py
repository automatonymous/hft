import pytest
import requests
from lib.authorization import CoinbaseExchangeAuth


def test_CoinbaseExchangeAuth():
    url = 'https://api.gdax.com/accounts'
    auth = CoinbaseExchangeAuth()
    response = requests.get(url, auth=auth)
    assert response.status_code == 200

