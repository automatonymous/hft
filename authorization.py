import hmac, time, base64
from requests.auth import AuthBase
from os import environ as env


class CoinbaseExchangeAuth(AuthBase):
    def __init__(self):
        self.api_key = env['GDAX_KEY']
        self.secret_key = env['GDAX_SECRET']
        self.passphrase = env['GDAX_PASSPHRASE']

    def __call__(self, request):
        timestamp = str(time.time())
        message = bytes(
            timestamp +
            request.method +
            request.path_url +
            (request.body or ''),
            'latin-1'
        )
        hmac_key = base64.b64decode(self.secret_key)
        signature = hmac.new(hmac_key, message)
        signature_b64 = base64.b64encode(
            bytes(signature.hexdigest(), 'latin-1')
        )

        request.headers.update({
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json',
        })
        return request

