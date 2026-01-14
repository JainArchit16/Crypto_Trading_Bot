import sys
from client import get_client
from validator import validate_symbol, validate_quantity, validate_price
from logger import logger

def place_limit_order(symbol, side, quantity, price):
    validate_symbol(symbol)
    validate_quantity(quantity)
    validate_price(price)

    client = get_client()
    response = client.futures_create_order(
    symbol=symbol,
    side=side,
    type="LIMIT",
    quantity=quantity,
    price=price,
    timeInForce="GTC"
)


    logger.info(f"Limit order placed: {response}")
    print(response)

if __name__ == "__main__":
    _, symbol, side, qty, price = sys.argv
    place_limit_order(symbol, side, float(qty), float(price))
