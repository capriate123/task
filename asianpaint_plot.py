import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from scipy.stats import t, zscore, norm

# Fetch historical data for a stock
def fetch_stock_data(ticker):
    stock_data = yf.Ticker(ticker).history(period="5y")
    stock_data['Daily_Return'] = stock_data['Close'].pct_change()
    return stock_data

# Perform statistical analysis and plot

def analyze_and_plot(stock_data, ticker):
    # Drop NaN values from returns
    daily_returns = stock_data['Daily_Return'].dropna()

    # Calculate T-score and Z-score for daily returns
    mean_return = daily_returns.mean()
    std_return = daily_returns.std()
    t_scores = (daily_returns - mean_return) / (std_return / np.sqrt(len(daily_returns)))
    z_scores = zscore(daily_returns)

    # Confidence Interval (95%)
    confidence_interval = (mean_return - 1.96 * std_return, mean_return + 1.96 * std_return)

    # Print the statistics
    print(f"--- Analysis for {ticker} ---")
    print(f"Mean Daily Return: {mean_return:.6f}")
    print(f"Standard Deviation of Returns: {std_return:.6f}")
    print(f"95% Confidence Interval for Daily Returns: {confidence_interval}")

    # Plot Probability Distributions
    plt.figure(figsize=(15, 5))

    # Daily Returns Distribution
    plt.subplot(1, 3, 1)
    plt.hist(daily_returns, bins=50, alpha=0.7, color='blue', density=True)
    x = np.linspace(daily_returns.min(), daily_returns.max(), 100)
    plt.plot(x, norm.pdf(x, mean_return, std_return), color='red', label='Normal Distribution')
    plt.title(f"Daily Returns Distribution ({ticker})")
    plt.xlabel("Daily Returns")
    plt.ylabel("Density")
    plt.legend()

    # T-score Distribution
    plt.subplot(1, 3, 2)
    plt.hist(t_scores, bins=50, alpha=0.7, color='green', density=True)
    x = np.linspace(t_scores.min(), t_scores.max(), 100)
    plt.plot(x, t.pdf(x, df=len(daily_returns)-1), color='red', label='T Distribution')
    plt.title(f"T-score Distribution ({ticker})")
    plt.xlabel("T-score")
    plt.ylabel("Density")
    plt.legend()

    # Z-score Distribution
    plt.subplot(1, 3, 3)
    plt.hist(z_scores, bins=50, alpha=0.7, color='purple', density=True)
    x = np.linspace(z_scores.min(), z_scores.max(), 100)
    plt.plot(x, norm.pdf(x, 0, 1), color='red', label='Standard Normal Distribution')
    plt.title(f"Z-score Distribution ({ticker})")
    plt.xlabel("Z-score")
    plt.ylabel("Density")
    plt.legend()

    plt.tight_layout()
    plt.show()

# Main execution for a specific stock
ticker = "ASIANPAINT.NS"  # Example stock
data = fetch_stock_data(ticker)
analyze_and_plot(data, ticker)
