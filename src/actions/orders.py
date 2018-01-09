from src.authorization import CoinbaseExchangeAuth
import requests
from json import dumps
from uuid import uuid4
from os import environ as env


def place_order(**kwargs):
    """Generic function for placing orders

    Args:
      **kwargs -> dict : necessary arguments for placing orders

    Returns:
      dict : order_id => response message
    """
    auth = CoinbaseExchangeAuth()
    request_body = kwargs
    client_oid = uuid4().hex
    request_body.update(dict(
        client_oid=client_oid,
        stp='co'
    ))
    response = requests.post(
        env['GDAX_URL']+'orders',
        data=dumps(request_body),
        auth=auth
    )
    return {client_oid:response.json()}


def market_order(side, product, size, unit):
    """Places market order with the given attributes.

    Args:
      side -> str : 'buy' or 'sell'
      product -> str : Pair of currencies to exchange, e.g. 'BTC-USD'
      size -> str : Quantity of the order, as specified by 'unit'
      unit -> str : 'size' or 'funds'

    Returns:
      dict : order_id => response message
    """
    args = {
        'type': 'market',
        'side': side,
        'product_id': product,
        unit: size
    }
    return place_order(**args)


def limit_order(side, product, price, size,
                tif='GTC', cancel_after=None, post_only=None):
    """Places limit order with the given attributes.

    Args:
      side -> str : 'buy' or 'sell'
      product -> str : Pair of currencies to exchange, e.g. 'BTC-USD'
      price -> str : Price per currency
      size -> str : Amount of product to buy or sell
      tif -> str : (Time in force) GTC, GTT, IOC, FOK
      cancel_after ->  str : min, hour, day
      post_only -> bool : Indicates if orders should only make liquidity

    Returns:
      dict : order_id => response message
    """
    args = {
        'type': 'limit',
        'side': side,
        'product_id': product,
        'price': price,
        'size': size,
        'time_in_force': tif,
        'cancel_after': cancel_after,
        'post_only': post_only
    }
    args = {k:v for k,v in args.items() if v}
    return place_order(**args)


def stop_order(side, product, price, size, unit):
    """Places stop order with the given attributes.

    Args:
      side -> str : 'buy' or 'sell'
      product -> str : Pair of currencies to exchange, e.g. 'BTC-USD'
      price -> str : Price at which the stop order triggers
      size -> str : Quantity of the order, as specified by 'unit'
      unit -> str : 'size' or 'funds'

    Returns:
      dict : order_id => response message
    """
    args = {
        'type': 'market',
        'side': side,
        'product_id': product,
        unit: size
    }
    return place_order(**args)


def cancel_order(order_id):
    """Cancels an order

    Args:
      order_id -> str : An order_id

    Returns:
      int : Status code, e.g. 200
    """
    auth = CoinbaseExchangeAuth()
    response = requests.delete(
        f"{env['GDAX_URL']}/orders/{order_id}",
        auth=auth
    )
    return response.status_code


def cancel_all(product=None):
    """Cancels all orders, or all for a given product

    Args:
      product -> str or None : A particular currency for which to cancel orders

    Returns:
      int : Status code, e.g. 200
    """
    auth = CoinbaseExchangeAuth()
    req_body = {product_id: product} if product else {}
    response = requests.delete(
        f"{env['GDAX_URL']}/orders",
        data=dumps(req_body),
        auth=auth
    )
    return response.status_code

