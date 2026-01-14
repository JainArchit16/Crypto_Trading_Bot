def validate_symbol(symbol: str):
    if not symbol.endswith("USDT"):
        raise ValueError("Only USDT-M futures supported")

def validate_quantity(qty: float):
    if qty <= 0:
        raise ValueError("Quantity must be > 0")

def validate_price(price: float):
    if price <= 0:
        raise ValueError("Price must be > 0")
