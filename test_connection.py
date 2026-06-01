from dotenv import load_dotenv
from binance.client import Client
import os

load_dotenv()

api_key = os.getenv("BINANCE_API_KEY")
secret_key = os.getenv("BINANCE_SECRET_KEY")

client = Client(api_key, secret_key)

client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"

try:
    account = client.futures_account()
    print("Connected Successfully!")
    print(account["availableBalance"])

except Exception as e:
    print("Failed:", e)