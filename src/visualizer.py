"""Plotly charts for technical analysis (dark theme)."""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go


def plot_candlestick(df: pd.DataFrame, ticker: str) -> go.Figure:
    """Interactive candlestick with SMA_20 and SMA_50 overlays."""
    fig = go.Figure()

    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
            name=ticker,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["SMA_20"],
            mode="lines",
            name="SMA 20",
            line=dict(color="#00bcd4", width=1.5),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["SMA_50"],
            mode="lines",
            name="SMA 50",
            line=dict(color="#ff9800", width=1.5),
        )
    )

    fig.update_layout(
        template="plotly_dark",
        title=f"{ticker} — Candlestick & Moving Averages",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        xaxis_rangeslider_visible=False,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=500,
    )
    return fig


def plot_rsi(df: pd.DataFrame) -> go.Figure:
    """14-day RSI with overbought (70) and oversold (30) reference lines."""
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["RSI"],
            mode="lines",
            name="RSI (14)",
            line=dict(color="#9c27b0", width=2),
        )
    )
    fig.add_hline(
        y=70,
        line_dash="dash",
        line_color="red",
        annotation_text="Overbought (70)",
        annotation_position="right",
    )
    fig.add_hline(
        y=30,
        line_dash="dash",
        line_color="green",
        annotation_text="Oversold (30)",
        annotation_position="right",
    )

    fig.update_layout(
        template="plotly_dark",
        title="Relative Strength Index (14-day)",
        xaxis_title="Date",
        yaxis_title="RSI",
        yaxis=dict(range=[0, 100]),
        height=400,
    )
    return fig
