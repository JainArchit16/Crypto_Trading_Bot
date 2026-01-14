from binance.client import Client
from config import BINANCE_API_KEY, BINANCE_API_SECRET
import time

def get_client(testnet=True):
    client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)

    if testnet:
        client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"
    else:
        print("Enable Testnet")
        return 

    # ---- FIX TIMESTAMP ISSUE ----
    server_time = client.get_server_time()
    local_time = int(time.time() * 1000)
    client.timestamp_offset = server_time["serverTime"] - local_time
    # --------------------------------

    return client
