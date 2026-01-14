def place_stop_limit(symbol, side, quantity, stop_price, limit_price, client):
    return client.new_order(
        symbol=symbol,
        side=side,
        type="STOP",
        quantity=quantity,
        price=limit_price,
        stopPrice=stop_price,
        timeInForce="GTC"
    )
