import yfinance as yf
import pandas as pd
import numpy as np

def compute_rsi(series, window=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def analyze_stock(ticker: str, capital: float):
    
    data = yf.download(ticker, period="2y", interval="1d", progress=False)

    if data.empty:
        return {"error": f"No data found for ticker {ticker}"}

    data["MA50"] = data["Close"].rolling(50).mean()
    data["MA200"] = data["Close"].rolling(200).mean()
    data["RSI"] = compute_rsi(data["Close"])

    latest = data.iloc[-1]

    trend = "Bullish" if latest["Close"] > latest["MA200"] else "Bearish"

    buy_condition = (
        latest["Close"] > latest["MA200"] and
        latest["MA50"] > latest["MA200"] and
        latest["RSI"] < 45
    )

    sell_condition = (
        latest["Close"] < latest["MA50"] or
        latest["RSI"] > 75
    )

    risk = capital * 0.05
    stop_distance = 0.08
    position_size = risk / stop_distance
    stop_price = latest["Close"] * (1 - stop_distance)

    if buy_condition:
        signal = "BUY"
        reason = "Uptrend + RSI pullback"
    elif sell_condition:
        signal = "SELL"
        reason = "Momentum weakening or overbought"
    else:
        signal = "HOLD"
        reason = "No strong setup"

    return {
        "ticker": ticker,
        "signal": signal,
        "reason": reason,
        "price": round(float(latest["Close"]), 2),
        "trend": trend,
        "rsi": round(float(latest["RSI"]), 2),
        "position_size": round(position_size, 2),
        "stop_price": round(float(stop_price), 2)
    }
