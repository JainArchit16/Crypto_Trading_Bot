def place_oco(symbol, side, qty, take_profit, stop_loss, client):
    tp = client.new_order(
        symbol=symbol,
        side=side,
        type="LIMIT",
        quantity=qty,
        price=take_profit,
        timeInForce="GTC"
    )

    sl = client.new_order(
        symbol=symbol,
        side=side,
        type="STOP_MARKET",
        stopPrice=stop_loss,
        quantity=qty
    )

    return {"tp": tp, "sl": sl}
