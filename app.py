import pandas as pd
import pandas_datareader.data as web
import datetime
import streamlit as st
from ta.momentum import RSIIndicator

st.set_page_config(page_title="UK ISA Trading Signal Dashboard", layout="wide")

def get_data(ticker):
    end = datetime.date.today()
    start = end - datetime.timedelta(days=365*2)
    try:
        df = web.DataReader(ticker, "yahoo", start, end)
    except Exception:
        return None
    return df

def analyze_stock(ticker, capital):
    data = get_data(ticker)
    if data is None or data.empty:
        return None, "Unable to load data for ticker"

    data["MA50"] = data["Close"].rolling(50).mean()
    data["MA200"] = data["Close"].rolling(200).mean()
    data["RSI"] = RSIIndicator(data["Close"], window=14).rsi()
    latest = data.iloc[-1]

    trend = "Bullish" if latest["Close"] > latest["MA200"] else "Bearish"

    buy_condition = (
        latest["Close"] > latest["MA200"] and
        data["MA50"].iloc[-1] > data["MA200"].iloc[-1] and
        latest["RSI"] < 45
    )
    sell_condition = (
        latest["Close"] < data["MA50"].iloc[-1] or
        latest["RSI"] > 75
    )

    risk = capital * 0.05
    stop_distance = 0.08
    position_size = risk / stop_distance
    stop_price = latest["Close"] * (1 - stop_distance)

    if buy_condition:
        signal = "BUY"
        reason = "Trend up + RSI pullback"
    elif sell_condition:
        signal = "SELL"
        reason = "Trend weakening or overbought"
    else:
        signal = "HOLD"
        reason = "No strong signal"

    return {
        "signal": signal,
        "reason": reason,
        "price": round(latest["Close"], 2),
        "trend": trend,
        "position_size": round(position_size, 2),
        "stop_price": round(stop_price, 2),
        "rsi": round(latest["RSI"], 2)
    }, None

# Streamlit UI
st.title("UK ISA Trading Signal Dashboard")

ticker = st.text_input("Enter LSE Ticker (eg BP.L, HSBA.L)", "BP.L")
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
        st.subheader("Price & Trend")
        st.write("Price:", result["price"])
        st.write("Trend:", result["trend"])
        st.write("RSI:", result["rsi"])
        st.subheader("Risk Management")
        st.write("Position Size (£):", result["position_size"])
        st.write("Stop Price:", result["stop_price"])

