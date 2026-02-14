import yfinance as yf
import pandas as pd
import streamlit as st

# Optional: install ta if needed
try:
    import ta
except ImportError:
    st.warning("ta library not installed. Install via requirements.txt")

st.set_page_config(page_title="UK ISA Signal Dashboard", layout="wide")

def analyze_stock(ticker, capital):
    # Download historical data
    data = yf.download(ticker, period="2y", interval="1d")
    if data.empty:
        return None, "Ticker invalid or no data found."

    # Compute indicators
    data["MA50"] = data["Close"].rolling(50).mean()
    data["MA200"] = data["Close"].rolling(200).mean()
    data["RSI"] = ta.momentum.RSIIndicator(data["Close"], window=14).rsi()
    data["VolumeMA"] = data["Volume"].rolling(20).mean()

    latest = data.iloc[-1]
    trend = "Bullish" if latest["Close"] > latest["MA200"] else "Bearish"

    buy_condition = (
        latest["Close"] > latest["MA200"] and
        latest["MA50"] > latest["MA200"] and
        latest["RSI"] < 45 and
        latest["Volume"] > latest["VolumeMA"]
    )

    sell_condition = (
        latest["Close"] < latest["MA50"] or
        latest["RSI"] > 75
    )

    risk_per_trade = capital * 0.05
    stop_distance = 0.08
    position_size = risk_per_trade / stop_distance
    stop_price = latest["Close"] * (1 - stop_distance)

    if buy_condition:
        signal = "BUY"
        reason = "Uptrend + RSI pullback + Volume confirmation"
    elif sell_condition:
        signal = "SELL"
        reason = "Momentum weakening or overbought"
    else:
        signal = "HOLD"
        reason = "No high-probability setup"

    return {
        "signal": signal,
        "reason": reason,
        "price": round(latest["Close"], 2),
        "rsi": round(latest["RSI"], 2),
        "trend": trend,
        "position_size": round(position_size, 2),
        "stop_price": round(stop_price, 2)
    }, None

# Streamlit UI
st.title("UK ISA Trading Signal Dashboard")

ticker = st.text_input("Enter LSE Ticker (example: BP.L, RR.L, HSBA.L)", "BP.L")
capital = st.number_input("Capital (£)", value=500)

if st.button("Analyze"):
    result, error = analyze_stock(ticker, capital)
    if error:
        st.error(error)
    else:
        st.subheader("Signal")
        st.markdown(f"## {result['signal']}")
        st.subheader("Reason")
        st.write(result["reason"])
        st.subheader("Market Data")
        st.write("Trend:", result["trend"])
        st.write("Price:", result["price"])
        st.write("RSI:", result["rsi"])
        st.subheader("Risk Management")
        st.write("Suggested Position Size (£):", result["position_size"])
        st.write("Suggested Stop Price:", result["stop_price"])
