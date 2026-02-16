# signal_engine.py
import yfinance as yf
import pandas as pd

def get_currency_symbol(ticker):
    """Detects the currency symbol from Yahoo Finance ticker info."""
    info = yf.Ticker(ticker).info
    currency = info.get("currency", "GBP")
    if currency == "USD":
        return "$"
    elif currency == "GBP":
        return "£"
    elif currency == "EUR":
        return "€"
    else:
        return currency  # fallback

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -1 * delta.clip(upper=0)
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def analyze_stock(ticker, capital):
    # Fetch historical data
    df = yf.download(ticker, period="2y", interval="1d")
    if df.empty:
        return {"error": "No data found for ticker"}

    # Calculate 200-day moving average
    df["MA200"] = df["Close"].rolling(window=200).mean()

    # Calculate RSI
    df["RSI"] = calculate_rsi(df["Close"])

    # Take the last row
    latest = df.tail(1).squeeze()  # .squeeze() converts single-row DataFrame to Series

    # Trend
    trend = "Bullish" if latest["Close"] > latest["MA200"] else "Bearish"

    # Signal
    if latest["RSI"] < 30:
        signal = "BUY"
        reason = "Oversold"
    elif latest["RSI"] > 70:
        signal = "SELL"
        reason = "Overbought"
    else:
        signal = "HOLD"
        reason = "No strong edge detected"

    # Position size & risk
    risk_per_trade = 25  # fixed risk per trade
    position_size = min(capital, 500)  # simple logic for demo
    stop_price = latest["Close"] * 0.92 if signal == "BUY" else latest["Close"] * 1.08

    # Currency
    currency_symbol = get_currency_symbol(ticker)

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
        "currency": currency_symbol
    }
