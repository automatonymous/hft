from os import environ as env
from json import dumps
from uuid import uuid4
import asyncio


async def place_order(auth, session, **kwargs):
    """Generic function for placing orders

    Args:
      auth -> CoinBaseExchangeAuth : A coinbase exchange auth object
      session -> aiohttp.ClientSession : An aiohttp client session
      **kwargs -> dict : necessary arguments for placing orders

    Returns:
      dict : order_id => response message
    """
    request_body = kwargs
    client_oid = uuid4().hex
    request_body.update(dict(
        client_oid=client_oid,
        stp='co'
    ))
    response = await session.post(
        env['GDAX_URL']+'orders',
        data=dumps(request_body),
        auth=auth
    )
    return {client_oid:response.json()}


async def market_order(auth, session, side, product, size, unit):
    """Places market order with the given attributes.

    Args:
      auth -> CoinBaseExchangeAuth : A coinbase exchange auth object
      session -> aiohttp.ClientSession : An aiohttp client session
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
    return await place_order(auth, session, **args)


async def limit_order(auth, session, side, product, price, size,
                tif='GTC', cancel_after=None, post_only=None):
    """Places limit order with the given attributes.

    Args:
      auth -> CoinBaseExchangeAuth : A coinbase exchange auth object
      session -> aiohttp.ClientSession : An aiohttp client session
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
    return await place_order(auth, session, **args)


async def stop_order(auth, session, side, product, price, size, unit):
    """Places stop order with the given attributes.

    Args:
      auth -> CoinBaseExchangeAuth : A coinbase exchange auth object
      session -> aiohttp.ClientSession : An aiohttp client session
      side -> str : 'buy' or 'sell'
      product -> str : Pair of currencies to exchange, e.g. 'BTC-USD'
      price -> str : Price at which the stop order triggers
      size -> str : Quantity of the order, as specified by 'unit'
      unit -> str : 'size' or 'funds'

    Returns:
      dict : order_id => response message
    """
    args = {
        'type': 'stop',
        'side': side,
        'product_id': product,
        unit: size
    }
    return await place_order(auth, session, **args)


async def cancel_order(auth, session, order_id):
    """Cancels an order

    Args:
      auth -> CoinBaseExchangeAuth : A coinbase exchange auth object
      session -> aiohttp.ClientSession : An aiohttp client session
      order_id -> str : An order_id

    Returns:
      int : Status code, e.g. 200
    """
    response = await session.delete(
        f"{env['GDAX_URL']}/orders/{order_id}",
        auth=auth
    )
    return response.status_code


aync def cancel_all(auth, session, product=None):
    """Cancels all orders, or all for a given product

    Args:
      auth -> CoinBaseExchangeAuth : A coinbase exchange auth object
      session -> aiohttp.ClientSession : An aiohttp client session
      product -> str or None : A particular currency for which to cancel orders

    Returns:
      int : Status code, e.g. 200
    """
    req_body = {product_id: product} if product else {}
    response = await session.delete(
        f"{env['GDAX_URL']}/orders",
        data=dumps(req_body),
        auth=auth
    )
    return response.status_code

