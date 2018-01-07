from src.authorization import CoinbaseExchangeAuth
from os import environ as env
import requests


def gets(route):
    url = env['GDAX_URL']+route
    auth = CoinbaseExchangeAuth()
    response = requests.get(url, auth=auth)
    return response.json()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Gets info from GDAX')
    parser.add_argument('route', metavar='rte',
                        type=str, nargs=1,
                        help='The route to hit')
    arg = parser.parse_args().route[0]
    print(gets(arg))

