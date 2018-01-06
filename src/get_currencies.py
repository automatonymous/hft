from authorization import CoinbaseExchangeAuth
import requests


def get_currencies():
    url = 'https://api.gdax.com/currencies'
    auth = CoinbaseExchangeAuth()
    response = requests.get(url, auth=auth)
    return response.json()

if __name__ == '__main__':
    for x in get_currencies():
        print(x)

