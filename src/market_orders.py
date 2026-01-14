import sys
from client import get_client
from validator import validate_symbol, validate_quantity
from logger import logger

def place_market_order(symbol, side, quantity):
    validate_symbol(symbol)
    validate_quantity(quantity)

    client = get_client()

    response = client.futures_create_order(
        symbol=symbol,
        side=side,
        type="MARKET",
        quantity=quantity
    )

    logger.info(f"Market order executed: {response}")
    print(response)


if __name__ == "__main__":
    _, symbol, side, qty = sys.argv
    place_market_order(symbol, side, float(qty))
