import yfinance as yf
import pandas as pd
import numpy as np
import ta

def analyze_stock(ticker: str, capital: float):
    # Download data safely
    data = yf.download(ticker, period="2y", interval="1d", progress=False)
    if data.empty:
        return {"error": f"No data found for ticker {ticker}"}

    # Calculate indicators
    data["MA50"] = data["Close"].rolling(50).mean()
    data["MA200"] = data["Close"].rolling(200).mean()
    data["RSI"] = ta.momentum.RSIIndicator(data["Close"], window=14).rsi()
    data["VolumeMA"] = data["Volume"].rolling(20).mean()

    # Take the last available row
    latest = data.iloc[-1]

    # Ensure floats for comparison
    close = float(latest["Close"])
    ma50 = float(latest["MA50"])
    ma200 = float(latest["MA200"])
    rsi = float(latest["RSI"])
    volume = float(latest["Volume"])
    volume_ma = float(latest["VolumeMA"])

    # Buy / Sell / Hold logic
    buy_condition = (
        (close > ma200) and
        (ma50 > ma200) and
        (rsi < 45) and
        (volume > volume_ma)
    )

    sell_condition = (
        (close < ma50) or
        (rsi > 75)
    )

    if buy_condition:
        signal = "BUY"
        reason = "Uptrend confirmed + RSI pullback + volume support"
    elif sell_condition:
        signal = "SELL"
        reason = "Momentum weakening or overbought condition"
    else:
        signal = "HOLD"
        reason = "No strong edge detected"

    # Trend
    trend = "Bullish" if close > ma200 else "Bearish"

    # Risk management
    risk_per_trade = capital * 0.05
    stop_distance = 0.08  # 8% stop
    position_size = risk_per_trade / stop_distance

    return {
        "ticker": ticker,
        "signal": signal,
        "reason": reason,
        "price": round(close, 2),
        "trend": trend,
        "rsi": round(rsi, 2),
        "position_size": round(position_size, 2),
        "risk_per_trade": round(risk_per_trade, 2),
        "stop_price": round(close * (1 - stop_distance), 2)
    }
