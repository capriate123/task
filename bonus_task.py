import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller, kpss

# Fetch historical data for a stock
def fetch_stock_data(ticker):
    stock_data = yf.Ticker(ticker).history(start="2023-01-01", end="2024-01-01")
    stock_data['Daily_Return'] = stock_data['Close'].pct_change()
    return stock_data

# Perform stationarity tests

def test_stationarity(stock_data, ticker):
    # Use closing prices for stationarity tests
    closing_prices = stock_data['Close'].dropna()

    # Augmented Dickey-Fuller Test
    adf_result = adfuller(closing_prices)
    print(f"ADF Test for {ticker}:")
    print(f"ADF Statistic: {adf_result[0]:.4f}")
    print(f"p-value: {adf_result[1]:.4f}")
    print("Critical Values:")
    for key, value in adf_result[4].items():
        print(f"   {key}: {value:.4f}")
    print("Stationary" if adf_result[1] <= 0.05 else "Non-Stationary")

    # KPSS Test
    kpss_result = kpss(closing_prices, regression='c')
    print(f"\nKPSS Test for {ticker}:")
    print(f"KPSS Statistic: {kpss_result[0]:.4f}")
    print(f"p-value: {kpss_result[1]:.4f}")
    print("Critical Values:")
    for key, value in kpss_result[3].items():
        print(f"   {key}: {value:.4f}")
    print("Stationary" if kpss_result[1] > 0.05 else "Non-Stationary")

# Main execution for selected stocks
stocks = ["RELIANCE.NS", "TCS.NS"]  # Example stocks

for ticker in stocks:
    print(f"\n--- Analysis for {ticker} ---")
    stock_data = fetch_stock_data(ticker)
    test_stationarity(stock_data, ticker)
