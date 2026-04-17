import os
import pandas as pd
from dotenv import load_dotenv
from binance.client import Client
from ta.trend import EMAIndicator
from ta.momentum import RSIIndicator

# Load API keys
load_dotenv()
api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")

# Connect to Binance Testnet
client = Client(api_key, api_secret)
client.API_URL = "https://testnet.binance.vision/api"

symbol = "XRPUSDT"
interval = Client.KLINE_INTERVAL_4HOUR
limit = 300

# Get data
klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)

df = pd.DataFrame(klines, columns=[
    "open_time", "open", "high", "low", "close", "volume",
    "close_time", "quote_asset_volume", "number_of_trades",
    "taker_buy_base", "taker_buy_quote", "ignore"
])

# Convert types
for col in ["open", "high", "low", "close", "volume"]:
    df[col] = df[col].astype(float)

# Indicators
df["ema50"] = EMAIndicator(close=df["close"], window=50).ema_indicator()
df["ema200"] = EMAIndicator(close=df["close"], window=200).ema_indicator()
df["rsi"] = RSIIndicator(close=df["close"], window=14).rsi()

# Last candles
last = df.iloc[-1]
prev = df.iloc[-2]

# Strategy
signal = "NO SIGNAL"

if last["ema50"] > last["ema200"] and prev["rsi"] < 40 and last["rsi"] > prev["rsi"]:
    signal = "BUY"
elif last["rsi"] > 65 or last["close"] < last["ema50"]:
    signal = "SELL"

# Output
print(f"{symbol}")
print(f"Close: {last['close']}")
print(f"EMA50: {last['ema50']:.6f}")
print(f"EMA200: {last['ema200']:.6f}")
print(f"RSI: {last['rsi']:.2f}")
print(f"Signal: {signal}")
