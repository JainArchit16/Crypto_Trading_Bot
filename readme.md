# Binance Futures Trading Bot (Testnet)

## Overview

This project is a **CLI-based trading bot** for **Binance USDT-M Futures**, built as part of a Python Developer assignment.
It supports **core order types**, **advanced order strategies**, and a **menu-driven CLI interface** with proper validation, logging, and testnet safety.

All trading is performed on **Binance Futures Testnet** using simulated funds.

---

## Features

### Core Orders (Mandatory)

- Market Orders
- Limit Orders

### Advanced Orders (Bonus)

- Stop-Limit Orders
- OCO (One-Cancels-the-Other) – simulated for Futures
- TWAP (Time-Weighted Average Price)

### Additional Functionality

- Menu-driven CLI interface
- View open orders and positions
- Cancel all open orders
- Close all open positions safely
- Input validation and error handling
- Structured logging to file (`bot.log`)
- Testnet-only execution (no real funds)

---

## Project Structure

```
project_root/
│
├── src/
│   ├── config.py          # Environment configuration
│   ├── client.py          # Binance client with testnet + time sync
│   ├── logger.py          # Structured logging setup
│   ├── validator.py       # Input validation helpers
│   ├── market_orders.py   # Market order logic
│   ├── limit_orders.py    # Limit order logic
│   ├── ui.py              # Menu-driven CLI interface
│   └── advanced/
│       ├── stop_limit.py
│       ├── oco.py
│       └── twap.py
│
├── bot.log                # Runtime logs
├── README.md
└── report.pdf             # Analysis & screenshots
```

---

## Prerequisites

- Python **3.9 or higher**
- Binance account (for testnet access)
- Internet connection

---

## Installation

Install required dependency:

```bash
pip install python-binance
```

---

## Binance Futures Testnet Setup

### 1. Open Testnet

Visit:

```
https://testnet.binancefuture.com/
```

Log in using your Binance account.

### 2. Create API Keys

- Go to **Profile → API Management**
- Create a new API key
- Enable **Futures**
- Copy the **API Key** and **Secret Key**

---

## Set API Keys

- Open `src/config.py`
- Paste the **API Key** and **Secret Key**

---

## Testnet Configuration

The bot is configured to use **Binance Futures Testnet** by default.

In `src/client.py`:

- Testnet base URL is set
- Server time is synced to prevent timestamp errors

This ensures:

- No real funds are used
- Requests are accepted reliably by Binance

---

## Running the Bot

Navigate to the project root and run:

```bash
python src/ui.py
```

---

## CLI Menu Options

```
1. Place Market Order
2. Place Limit Order
3. View Open Orders
4. View Positions
5. Cancel All Open Orders
6. Close All Open Positions
7. Execute TWAP Order
8. Place OCO Order
9. View All Orders
10. Exit
```

---

## Order Types Explained

### Market Order

Executes immediately at the current market price.

### Limit Order

Executes only at the specified price or better.

### TWAP (Time-Weighted Average Price)

Splits a large order into smaller market orders executed over time to reduce slippage.

### OCO (Simulated for Futures)

Places:

- One **LIMIT** order (take profit)
- One **STOP_MARKET** order (stop loss)

Binance Futures does not support native OCO, so this is implemented as coordinated orders.

---

## Viewing Orders

### Open Orders

Shows active LIMIT orders only.

### Conditional Orders

STOP / STOP_MARKET orders are conditional and **do not appear in open orders** until triggered.
They can be verified via:

- Binance Futures Testnet UI
- Order history endpoints (when available)

### View All Orders

Displays recent orders with:

- Order type
- Status
- Quantity and price
- Creation and update timestamps (UTC)

Note: On testnet, historical order data may be limited or cleared periodically.

---

## Logging

All actions are logged to `bot.log`, including:

- Order placement
- Order cancellation
- Position closures
- Errors and exceptions

Log format includes timestamps for traceability.

---

## Safety Notes

- All trading is done on **Binance Futures Testnet**
- No real funds are used
- API keys are loaded from environment variables (never hardcoded)
- Positions can be closed instantly using the CLI

---

## Testing & Verification

The bot was tested by:

- Placing and closing market orders
- Creating visible limit orders
- Executing TWAP strategies
- Simulating OCO orders
- Verifying positions and orders via Binance Testnet UI
- Reviewing logs for correctness

Screenshots and explanations are included in `report.pdf`.

---

## Notes on Binance Futures Behavior

- STOP / STOP_MARKET orders are conditional and hidden until triggered
- Testnet order history may be inconsistent
- Market orders may briefly appear as `NEW` before filling on testnet

These behaviors are expected and handled correctly by the bot.

---

## Conclusion

This project demonstrates:

- Clean Python architecture
- Proper API usage
- Defensive input validation
- Real-world trading system behavior
- Practical CLI-based usability

---
