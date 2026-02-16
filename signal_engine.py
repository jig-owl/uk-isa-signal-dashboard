# signal_engine.py
import yfinance as yf
import pandas as pd
import numpy as np

def currency_symbol(curr):
    """Convert currency code to symbol."""
    return {"USD":"$", "GBP":"£", "EUR":"€"}.get(curr, curr)

def analyze_stock(ticker: str, capital: float):
    # Download historical data
    df = yf.download(ticker, period="2y", interval="1d")
    if df.empty:
        return {"error": "Ticker not found or no data available"}

    # Calculate simple moving average
    df["MA200"] = df["Close"].rolling(window=200).mean()
    
    # Relative Strength Index (RSI)
    delta = df["Close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    df["RSI"] = 100 - (100 / (1 + rs))
    
    latest = df.iloc[-1]

    # Determine trend
    trend = "Bullish" if latest["Close"] > latest["MA200"] else "Bearish"

    # Simple trading signal
    if latest["RSI"] < 30:
        signal = "BUY"
        reason = "Oversold"
    elif latest["RSI"] > 70:
        signal = "SELL"
        reason = "Overbought or momentum weakening"
    else:
        signal = "HOLD"
        reason = "No strong edge detected"

    # Risk and position sizing
    risk_per_trade = 25.0  # can be parameterized
    stop_price = latest["Close"] * 0.92  # example: 8% stop
    position_size = capital * (risk_per_trade / 100) / (latest["Close"] - stop_price)

    # Detect currency dynamically
    ticker_info = yf.Ticker(ticker).info
    currency = currency_symbol(ticker_info.get("currency", "$"))

    return {
        "ticker": ticker,
        "signal": signal,
        "reason": reason,
        "price": round(latest["Close"], 2),
        "trend": trend,
        "rsi": round(latest["RSI"], 2),
        "position_size": round(position_size, 2),
        "risk_per_trade": round(risk_per_trade, 2),
        "stop_price": round(stop_price, 2),
        "currency": currency
    }
