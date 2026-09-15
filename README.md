# VSEC — Stock Market Analytics & ML Forecasting Dashboard

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-red)](https://streamlit.io/)

Interactive dashboard for **technical analysis** and **machine-learning price forecasting** on US equities. Fetches live historical data from Yahoo Finance, computes indicators (SMA, RSI, volatility), and trains a **Prophet** model for forward-looking predictions with confidence bands.

**Repository:** [github.com/saishnimbalkar397/VSEC](https://github.com/saishnimbalkar397/VSEC)

## Tech Stack

| Layer | Tools |
|--------|--------|
| Language | Python |
| UI | Streamlit |
| Data | yFinance, Pandas, NumPy |
| Charts | Plotly (`plotly_dark`) |
| Forecasting | Meta Prophet |

## Features

- Historical OHLCV download for any valid ticker symbol
- **Technical indicators:** 20/50-day SMA, daily returns, 20-day annualized volatility, 14-day RSI
- **Visualizations:** candlestick + moving averages, RSI with overbought/oversold levels
- **ML forecast:** configurable horizon (7–90 days) with uncertainty intervals
- Summary metrics: latest close, daily change, volatility, RSI

## Project Structure

```
├── src/
│   ├── __init__.py
│   ├── data_loader.py       # yFinance fetch + indicators
│   ├── visualizer.py        # Plotly technical charts
│   └── predictor.py         # Prophet training & forecast plots
├── app.py                   # Streamlit entry point
├── requirements.txt
└── README.md
```

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/saishnimbalkar397/VSEC.git
   cd VSEC
   ```

2. **Create and activate a virtual environment** (recommended):

   ```bash
   python -m venv .venv
   ```

   **Windows (PowerShell):**

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   **macOS / Linux:**

   ```bash
   source .venv/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

   > **Note:** Prophet may require a C++ compiler on some systems. On Windows, install [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) before `pip install prophet` if the build fails.

## Run the App

```bash
streamlit run app.py
```

Open the URL shown in the terminal (typically [http://localhost:8501](http://localhost:8501)).

### Usage

1. Enter a ticker symbol (default: `AAPL`).
2. Select a historical period (`6m`, `1y`, `2y`, `5y`).
3. Adjust the forecast horizon with the slider.
4. Click **Fetch & Analyze Data**.

## Disclaimer

This project is for **education and research only**. It is not financial advice. Past performance and model forecasts do not guarantee future results.

## Author

**Saish Nimbalkar** — [GitHub @saishnimbalkar397](https://github.com/saishnimbalkar397)
