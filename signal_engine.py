# signal_engine.py
import yfinance as yf
import pandas as pd
import numpy as np

def analyze_stock(ticker: str, capital: float):
    """
    Analyze a stock and return a trading signal with metrics.
    """

    # Download historical data
    df = yf.download(ticker, period="1y", interval="1d")
    if df.empty:
        return {"error": f"No data found for {ticker}"}

    # Calculate moving averages
    df["MA50"] = df["Close"].rolling(window=50).mean()
    df["MA200"] = df["Close"].rolling(window=200).mean()

    # Calculate RSI
    delta = df["Close"].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    df["RSI"] = 100 - (100 / (1 + rs))

    # Get the latest row
    latest = df.iloc[-1]

    # Trend determination (scalar comparison)
    trend = "Bullish" if latest["Close"] > latest["MA200"] else "Bearish"

    # Simple signal logic
    if latest["RSI"] < 30 and trend == "Bullish":
        signal = "BUY"
        reason = "Oversold but uptrend"
    elif latest["RSI"] > 70 and trend == "Bearish":
        signal = "SELL"
        reason = "Overbought and downtrend"
    else:
        signal = "HOLD"
        reason = "No strong edge detected"

    # Position sizing (example: 5% of capital per trade)
    risk_per_trade = 25  # Fixed for demo
    position_size = min(capital * 0.625, 312.5)  # Example cap

    # Stop price (10% buffer)
    stop_price = latest["Close"] * (0.9 if signal == "BUY" else 1.1)

    # Detect currency symbol dynamically from ticker ('.L' = GBP, else default USD)
    currency = "£" if ticker.upper().endswith(".L") else "$"

    # Build result
    result = {
        "ticker": ticker.upper(),
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

    return result
