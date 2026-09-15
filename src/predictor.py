"""Prophet-based price forecasting and visualization."""

from __future__ import annotations

from typing import Tuple

import pandas as pd
import plotly.graph_objects as go
from prophet import Prophet


def train_and_forecast(
    df: pd.DataFrame, days_to_predict: int = 30
) -> Tuple[Prophet, pd.DataFrame]:
    """
    Fit Prophet on Close prices and forecast future days.

    Returns:
        Tuple of (fitted Prophet model, forecast DataFrame including history + future).
    """
    ds = pd.Series(pd.to_datetime(df.index), name="ds")
    if ds.dt.tz is not None:
        ds = ds.dt.tz_localize(None)
    prophet_df = pd.DataFrame({"ds": ds, "y": df["Close"].values})

    model = Prophet(daily_seasonality=True, yearly_seasonality=True)
    model.fit(prophet_df)

    future = model.make_future_dataframe(periods=days_to_predict)
    forecast = model.predict(future)

    return model, forecast


def plot_forecast(
    df: pd.DataFrame, forecast: pd.DataFrame, ticker: str
) -> go.Figure:
    """Historical close, Prophet yhat, and confidence interval band."""
    hist_dates = pd.to_datetime(df.index)
    if getattr(hist_dates, "tz", None) is not None:
        hist_dates = hist_dates.tz_localize(None)

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=hist_dates,
            y=df["Close"],
            mode="lines",
            name="Historical Close",
            line=dict(color="#2196f3", width=2),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=forecast["ds"],
            y=forecast["yhat"],
            mode="lines",
            name="Forecast (yhat)",
            line=dict(color="#4caf50", width=2, dash="dot"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=forecast["ds"].tolist() + forecast["ds"].tolist()[::-1],
            y=forecast["yhat_upper"].tolist() + forecast["yhat_lower"].tolist()[::-1],
            fill="toself",
            fillcolor="rgba(76, 175, 80, 0.2)",
            line=dict(color="rgba(255,255,255,0)"),
            hoverinfo="skip",
            name="Confidence interval",
            showlegend=True,
        )
    )

    fig.update_layout(
        template="plotly_dark",
        title=f"{ticker} — Prophet Forecast",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        height=500,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig
