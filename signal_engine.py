import yfinance as yf
import pandas as pd

def get_currency(ticker: str) -> str:
    """Detect currency based on ticker suffix."""
    if ticker.endswith(".L"):
        return "£"
    else:
        return "$"

def analyze_stock(ticker: str, capital: float):
    # Fetch historical data
    data = yf.download(ticker, period="1y")
    if data.empty:
        raise ValueError(f"No data found for ticker {ticker}")

    # Calculate indicators
    data["MA200"] = data["Close"].rolling(window=200).mean()
    data["RSI"] = compute_rsi(data["Close"], window=14)

    latest = data.iloc[-1]

    # Signal logic
    signal = "HOLD"
    reason = "No strong edge detected"
    if latest["Close"] > latest["MA200"] and latest["RSI"] < 70:
        signal = "BUY"
        reason = "Price above 200-day MA and RSI not overbought"
    elif latest["Close"] < latest["MA200"] or latest["RSI"] > 70:
        signal = "SELL"
        reason = "Momentum weakening or overbought"

    # Trend (scalar comparison to avoid Series mismatch)
    trend = "Bullish" if latest["Close"] > latest["MA200"] else "Bearish"

    # Position sizing
    risk_per_trade = 25  # £ or $ per trade
    position_size = min(capital, 500)  # Example fixed position logic
    stop_price = latest["Close"] - (latest["Close"] * 0.08) if signal == "BUY" else latest["Close"] + (latest["Close"] * 0.08)

    currency = get_currency(ticker)

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

def compute_rsi(series: pd.Series, window: int = 14) -> pd.Series:
    """Calculate the Relative Strength Index (RSI)."""
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=window, min_periods=1).mean()
    avg_loss = loss.rolling(window=window, min_periods=1).mean()

    rs = avg_gain / (avg_loss + 1e-9)  # Avoid division by zero
    rsi = 100 - (100 / (1 + rs))
    return rsi
