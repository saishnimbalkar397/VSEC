"""Streamlit dashboard: stock analytics and ML forecasting."""

from __future__ import annotations

import streamlit as st

from src.data_loader import load_stock_data
from src.predictor import plot_forecast, train_and_forecast
from src.visualizer import plot_candlestick, plot_rsi

st.set_page_config(
    page_title="Stock Market Analytics & ML Forecast Dashboard",
    layout="wide",
)

st.title("Stock Market Analytics & Machine Learning Forecast Dashboard")
st.caption("Technical indicators, interactive charts, and Prophet-based price forecasts.")

with st.sidebar:
    st.header("Controls")
    ticker_input = st.text_input("Ticker symbol", value="AAPL").upper()
    period = st.selectbox(
        "Historical timeframe",
        options=["6m", "1y", "2y", "5y"],
        index=1,
    )
    days_to_predict = st.slider(
        "Forecast horizon (days)",
        min_value=7,
        max_value=90,
        value=30,
    )
    fetch_clicked = st.button("Fetch & Analyze Data", type="primary")

if fetch_clicked:
    with st.spinner(f"Loading data for {ticker_input}..."):
        try:
            df = load_stock_data(ticker_input, period=period)
        except ValueError as err:
            st.error(str(err))
            st.stop()
        except Exception as err:
            st.error(
                f"Unexpected error while fetching data: {err}. "
                "Please try again later."
            )
            st.stop()

    latest_close = float(df["Close"].iloc[-1])
    prev_close = float(df["Close"].iloc[-2]) if len(df) > 1 else latest_close
    daily_delta = latest_close - prev_close
    daily_pct = (daily_delta / prev_close * 100) if prev_close else 0.0
    vol_20 = float(df["Volatility_20"].iloc[-1])
    current_rsi = float(df["RSI"].iloc[-1])

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            label="Latest Close Price",
            value=f"${latest_close:,.2f}",
            delta=f"{daily_delta:+.2f} ({daily_pct:+.2f}%)",
        )
    with col2:
        st.metric(label="20-Day Volatility (ann.)", value=f"{vol_20:.2%}")
    with col3:
        st.metric(label="Current RSI (14)", value=f"{current_rsi:.1f}")

    st.subheader("1. Technical Analysis")
    st.plotly_chart(plot_candlestick(df, ticker_input), use_container_width=True)
    st.plotly_chart(plot_rsi(df), use_container_width=True)

    st.subheader("2. Machine Learning Forecast")
    with st.spinner("Training Prophet model..."):
        try:
            _model, forecast = train_and_forecast(df, days_to_predict=days_to_predict)
            st.plotly_chart(
                plot_forecast(df, forecast, ticker_input),
                use_container_width=True,
            )
        except Exception as err:
            st.error(f"Forecast failed: {err}")

    with st.expander("Raw historical data"):
        display_df = df.copy()
        display_df.index.name = "Date"
        st.dataframe(display_df, use_container_width=True)
else:
    st.info("Configure options in the sidebar and click **Fetch & Analyze Data**.")
