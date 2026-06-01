import argparse
import os

from dotenv import load_dotenv
from binance.client import Client

from orders import place_market_order, place_limit_order
from validators import validate_side, validate_order_type, validate_quantity
from logging_config import logger
import logging

load_dotenv()

api_key = os.getenv("BINANCE_API_KEY")
secret_key = os.getenv("BINANCE_SECRET_KEY")

if not api_key or not secret_key:
    raise ValueError("API keys missing in .env file")

client = Client(api_key, secret_key, testnet=True)

parser = argparse.ArgumentParser(description="Trading Bot CLI")

parser.add_argument("--symbol", required=True)
parser.add_argument("--side", required=True)
parser.add_argument("--type", required=True)
parser.add_argument("--quantity", type=float, required=True)
parser.add_argument("--price", type=float)

args = parser.parse_args()

# Normalize input (IMPORTANT FIX)
args.side = args.side.upper()
args.type = args.type.upper()

try:
    validate_side(args.side)
    validate_order_type(args.type)
    validate_quantity(args.quantity)

    logger.info(f"Request: {args.symbol} {args.side} {args.type}")

    order = None

    if args.type == "MARKET":
        order = place_market_order(
            client,
            args.symbol,
            args.side,
            args.quantity
        )

    elif args.type == "LIMIT":
        if args.price is None:
            raise ValueError("Price required for LIMIT order")

        order = place_limit_order(
            client,
            args.symbol,
            args.side,
            args.quantity,
            args.price
        )

    else:
        raise ValueError("Unsupported order type")

    # SAFE CHECK (IMPORTANT FIX)
    if not order:
        print("❌ Order failed or no response received")
        logger.error("Order returned None")
        exit()

    print("\n===== ORDER RESPONSE =====")
    print("Order ID     :", order.get("orderId", "N/A"))
    print("Status       :", order.get("status", "N/A"))
    print("Qty          :", order.get("origQty", "N/A"))
    print("Executed Qty :", order.get("executedQty", "N/A"))
    print("Avg Price    :", order.get("avgPrice", "N/A"))

    logger.info(order)

except Exception as e:
    logger.error(str(e))
    print("ERROR:", e)

finally:
    logging.shutdown()