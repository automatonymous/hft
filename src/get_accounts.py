from authorization import CoinbaseExchangeAuth
import requests


def get_accounts():
    url = 'https://api.gdax.com/accounts'
    auth = CoinbaseExchangeAuth()
    response = requests.get(url, auth=auth)
    return response.json()

if __name__ == '__main__':
    for x in get_accounts():
        print(x)

