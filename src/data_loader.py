"""Fetch stock history from yFinance and compute technical indicators."""

from __future__ import annotations

import pandas as pd
import yfinance as yf


def _compute_rsi(close: pd.Series, period: int = 14) -> pd.Series:
    """14-day Relative Strength Index using Wilder-style rolling means."""
    delta = close.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = (-delta).where(delta < 0, 0.0)
    avg_gain = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.rolling(window=period, min_periods=period).mean()
    rs = avg_gain / avg_loss.replace(0, float("nan"))
    rsi = 100 - (100 / (1 + rs))
    return rsi


def load_stock_data(ticker: str, period: str = "1y") -> pd.DataFrame:
    """
    Load historical OHLCV data for a ticker and append technical indicators.

    Args:
        ticker: Stock symbol (e.g. AAPL).
        period: yFinance history period (e.g. 6m, 1y, 2y, 5y).

    Returns:
        DataFrame with price columns and SMA_20, SMA_50, Daily_Return,
        Volatility_20, and RSI.

    Raises:
        ValueError: If ticker is invalid or no data is returned.
    """
    ticker = ticker.strip().upper()
    if not ticker:
        raise ValueError("Ticker symbol cannot be empty.")

    try:
        hist = yf.Ticker(ticker).history(period=period)
    except Exception as exc:
        raise ValueError(
            f"Failed to fetch data for '{ticker}'. Check the symbol and your connection."
        ) from exc

    if hist is None or hist.empty:
        raise ValueError(
            f"No historical data found for ticker '{ticker}'. "
            "Verify the symbol is valid and try a different timeframe."
        )

    df = hist.copy()
    df["SMA_20"] = df["Close"].rolling(window=20, min_periods=1).mean()
    df["SMA_50"] = df["Close"].rolling(window=50, min_periods=1).mean()
    df["Daily_Return"] = df["Close"].pct_change()
    df["Volatility_20"] = (
        df["Daily_Return"].rolling(window=20, min_periods=1).std() * (252**0.5)
    )
    df["RSI"] = _compute_rsi(df["Close"], period=14)

    return df
