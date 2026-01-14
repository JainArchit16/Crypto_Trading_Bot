import sys
from client import get_client
from market_orders import place_market_order
from limit_orders import place_limit_order
from validator import validate_symbol, validate_quantity, validate_price
from logger import logger
import time
from datetime import datetime

def input_symbol():
    while True:
        symbol = input("Symbol (e.g. BTCUSDT): ").strip().upper()
        try:
            validate_symbol(symbol)
            return symbol
        except Exception as e:
            print(f"Invalid symbol: {e}")

def input_side():
    while True:
        side = input("Side (BUY / SELL): ").strip().upper()
        if side in ["BUY", "SELL"]:
            return side
        print("Invalid side. Enter BUY or SELL.")

def input_quantity():
    while True:
        try:
            qty = float(input("Quantity: ").strip())
            validate_quantity(qty)
            return qty
        except ValueError:
            print("Quantity must be a number > 0.")
        except Exception as e:
            print(e)

def input_price():
    while True:
        try:
            price = float(input("Price: ").strip())
            validate_price(price)
            return price
        except ValueError:
            print("Price must be a number > 0.")
        except Exception as e:
            print(e)

def view_open_orders(client):
    orders = client.futures_get_open_orders()
    if not orders:
        print("No open orders.")
        return

    print("\nOPEN ORDERS")
    print("-" * 60)
    for o in orders:
        print(
            f"ID: {o['orderId']} | {o['symbol']} | {o['side']} | "
            f"Qty: {o['origQty']} | Price: {o['price']} | Status: {o['status']}"
        )
    print("-" * 60)

def view_positions(client):
    positions = client.futures_position_information()
    active = [p for p in positions if float(p["positionAmt"]) != 0]

    if not active:
        print("No open positions.")
        return

    print("\nOPEN POSITIONS")
    print("-" * 60)
    for p in active:
        print(
            f"{p['symbol']} | Amt: {p['positionAmt']} | "
            f"Entry: {p['entryPrice']} | PnL: {p['unRealizedProfit']}"
        )
    print("-" * 60)

def cancel_all_orders(client):
    symbol = input_symbol()
    client.futures_cancel_all_open_orders(symbol=symbol)
    logger.info(f"Cancelled all open orders for {symbol}")
    print(f"All open orders for {symbol} cancelled.")

def main_menu():
    print("\n==============================")
    print(" Binance Futures Trading Bot ")
    print(" (Testnet CLI UI)")
    print("==============================")
    print("1. Place Market Order")
    print("2. Place Limit Order")
    print("3. View Open Orders")
    print("4. View Positions")
    print("5. Cancel All Open Orders")
    print("6. Close All Open Positions")
    print("7. Execute TWAP Order")
    print("8. Place OCO Order")
    print("9. View All Orders")
    print("10. Exit")


def main():
    client = get_client()

    while True:
        try:
            main_menu()
            choice = input("Enter choice (1-10): ").strip()

            if choice == "1":
                symbol = input_symbol()
                side = input_side()
                qty = input_quantity()
                place_market_order(symbol, side, qty)

            elif choice == "2":
                symbol = input_symbol()
                side = input_side()
                qty = input_quantity()
                price = input_price()
                place_limit_order(symbol, side, qty, price)

            elif choice == "3":
                view_open_orders(client)

            elif choice == "4":
                view_positions(client)

            elif choice == "5":
                cancel_all_orders(client)

            elif choice == "6":
                close_all_positions(client)

            elif choice == "7":
                execute_twap_ui(client)

            elif choice == "8":
                place_oco_ui(client)

            elif choice == "9":
                view_all_orders(client)

            elif choice == "10":
                print("Exiting safely.")
                sys.exit(0)


            else:
                print("Invalid choice. Enter a number between 1 and 9.")

        except KeyboardInterrupt:
            print("\nGraceful exit.")
            sys.exit(0)
        except Exception as e:
            logger.error(str(e))
            print(f"Error: {e}")




def format_time(ms):
    if not ms:
        return "N/A"
    return datetime.utcfromtimestamp(ms / 1000).strftime("%Y-%m-%d %H:%M:%S UTC")


def view_all_orders(client):
    symbol = input_symbol()

    orders = client.futures_get_all_orders(symbol=symbol, limit=20)

    if not orders:
        print("No orders found.")
        return

    print("\nALL ORDERS (Active / Conditional / History)")
    print("-" * 110)

    for o in orders:
        created = format_time(o.get("time"))
        updated = format_time(o.get("updateTime"))

        order_type = o["type"]
        status = o["status"]
        stop_price = o.get("stopPrice", "0")

        extra = ""
        if order_type in ["STOP", "STOP_MARKET", "TAKE_PROFIT", "TAKE_PROFIT_MARKET"]:
            extra = f" | Trigger: {stop_price}"
        
        print("-"*80)

        print(
            f"ID: {o['orderId']} | {o['symbol']} | {o['side']} | {order_type} | "
            f"Qty: {o['origQty']} | Price: {o['price']} | "
            f"Status: {status}{extra}\n"
            f"   Created: {created} | Updated: {updated}"
        )

        print("-"*80)
        print()

    print("-" * 110)



def execute_twap_ui(client):
    symbol = input_symbol()
    side = input_side()

    while True:
        try:
            total_qty = float(input("Total Quantity: ").strip())
            validate_quantity(total_qty)
            break
        except Exception as e:
            print(e)

    while True:
        try:
            slices = int(input("Number of slices (>=2): ").strip())
            if slices < 2:
                raise ValueError("Slices must be >= 2")
            break
        except Exception as e:
            print(e)

    while True:
        try:
            interval = int(input("Interval between orders (seconds): ").strip())
            if interval < 1:
                raise ValueError("Interval must be >= 1 second")
            break
        except Exception as e:
            print(e)

    slice_qty = round(total_qty / slices, 6)

    print(f"\nExecuting TWAP: {slices} orders of {slice_qty} every {interval}s\n")

    for i in range(slices):
        client.futures_create_order(
            symbol=symbol,
            side=side,
            type="MARKET",
            quantity=slice_qty
        )
        logger.info(f"TWAP order {i+1}/{slices}: {symbol} {side} {slice_qty}")
        print(f"Executed slice {i+1}/{slices}")
        time.sleep(interval)

    print("TWAP execution completed.")


def place_oco_ui(client):
    symbol = input_symbol()
    side = input_side()
    qty = input_quantity()

    print("Take Profit Price:")
    take_profit = input_price()

    print("Stop Loss Price:")
    stop_loss = input_price()

    # Take profit LIMIT
    client.futures_create_order(
        symbol=symbol,
        side=side,
        type="LIMIT",
        quantity=qty,
        price=take_profit,
        timeInForce="GTC"
    )

    # Stop loss STOP-MARKET
    client.futures_create_order(
        symbol=symbol,
        side=side,
        type="STOP_MARKET",
        stopPrice=stop_loss,
        quantity=qty
    )

    logger.info(
        f"OCO simulated: {symbol} {side} TP={take_profit} SL={stop_loss}"
    )

    print("OCO orders placed (simulated on Futures).")

def close_all_positions(client):
    positions = client.futures_position_information()
    open_positions = [p for p in positions if float(p["positionAmt"]) != 0]

    if not open_positions:
        print("No open positions to close.")
        return

    print("\nCLOSING OPEN POSITIONS")
    print("-" * 60)

    for p in open_positions:
        symbol = p["symbol"]
        qty = abs(float(p["positionAmt"]))

        if qty == 0:
            continue

        side = "SELL" if float(p["positionAmt"]) > 0 else "BUY"

        client.futures_create_order(
            symbol=symbol,
            side=side,
            type="MARKET",
            quantity=qty
        )

        logger.info(f"Closed position: {symbol} | Side: {side} | Qty: {qty}")
        print(f"Closed {symbol} position with {side} {qty}")

    print("-" * 60)


if __name__ == "__main__":
    main()
