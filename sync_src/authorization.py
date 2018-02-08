import hmac, base64, hashlib
from requests.auth import AuthBase
import requests
from os import environ as env


class CoinbaseExchangeAuth(AuthBase):
    def __init__(self):
        self.api_key = env['GDAX_KEY']
        self.secret_key = env['GDAX_SECRET']
        self.passphrase = env['GDAX_PASSPHRASE']

    def __call__(self, request):
        timestamp = str(_server_time_())
        message = (
            timestamp +
            request.method +
            request.path_url +
            (request.body or '')
        )
        message = message.encode('ascii')
        hmac_key = base64.b64decode(self.secret_key)
        assert len(hmac_key) == 64
        signature = hmac.new(hmac_key, message, hashlib.sha256)
        signature_b64 = base64.b64encode(signature.digest())

        request.headers.update({
            'CB-ACCESS-SIGN': signature_b64.decode('ascii'),
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json',
        })
        return request


def get_auth_dict():
    timestamp = str(_server_time_())
    message = ( timestamp + 'GET' + '/users/self/verify' )
    message = message.encode('ascii')
    hmac_key = base64.b64decode(env['GDAX_SECRET'])
    assert len(hmac_key) == 64
    signature = hmac.new(hmac_key, message, hashlib.sha256)
    signature_b64 = base64.b64encode(signature.digest())
    return dict(
        signature = signature_b64.decode('ascii'),
        key = env['GDAX_KEY'],
        passphrase = env['GDAX_PASSPHRASE'],
        timestamp = timestamp
    )


def _server_time_():
    return requests.get(env['GDAX_URL'] + 'time').json()['epoch']


if __name__ == '__main__':
    print(get_auth_dict())

