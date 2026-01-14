import time

def execute_twap(symbol, side, total_qty, slices, interval, client):
    slice_qty = total_qty / slices

    for i in range(slices):
        client.new_order(
            symbol=symbol,
            side=side,
            type="MARKET",
            quantity=round(slice_qty, 3)
        )
        time.sleep(interval)
