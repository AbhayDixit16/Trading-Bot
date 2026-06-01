from dotenv import load_dotenv
from binance.client import Client
from orders import place_market_order, place_limit_order
import os

load_dotenv()

api_key = os.getenv("BINANCE_API_KEY")
secret_key = os.getenv("BINANCE_SECRET_KEY")

client = Client(api_key, secret_key, testnet=True)

print("=== TRADING BOT ===")

symbol = input("Enter Symbol (e.g BTCUSDT): ")
side = input("BUY or SELL: ")
order_type = input("MARKET or LIMIT: ")
quantity = float(input("Quantity: "))

price = None

if order_type == "LIMIT":
    price = float(input("Price: "))

if order_type == "MARKET":
    order = place_market_order(client, symbol, side, quantity)
else:
    order = place_limit_order(client, symbol, side, quantity, price)

print("\nORDER RESPONSE:")
print(order)