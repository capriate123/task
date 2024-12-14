import requests
from bs4 import BeautifulSoup
import yfinance as yf
import pandas as pd

# Define URLs and ticker symbols for selected Nifty50 stocks
stocks = [
    {"url": "https://www.screener.in/company/HDFCBANK/", "ticker": "HDFCBANK.NS"},
    {"url": "https://www.screener.in/company/RELIANCE/", "ticker": "RELIANCE.NS"},
    {"url": "https://www.screener.in/company/TCS/", "ticker": "TCS.NS"},
    {"url": "https://www.screener.in/company/INFY/", "ticker": "INFY.NS"},
    {"url": "https://www.screener.in/company/ASIANPAINT/", "ticker": "ASIANPAINT.NS"}
]

# Function to scrape data from Screener.in
def scrape_screener(stock_url):
    response = requests.get(stock_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    data = {}
    try:
        data['PE'] = soup.find('li', text=lambda x: x and 'P/E' in x).text.split(':')[-1].strip()
        data['EPS'] = soup.find('li', text=lambda x: x and 'EPS' in x).text.split(':')[-1].strip()
        data['52_Week_High'] = soup.find('li', text=lambda x: x and '52 Week High' in x).text.split(':')[-1].strip()
        data['52_Week_Low'] = soup.find('li', text=lambda x: x and '52 Week Low' in x).text.split(':')[-1].strip()
        data['Market_Cap'] = soup.find('li', text=lambda x: x and 'Market Cap' in x).text.split(':')[-1].strip()
    except AttributeError:
        print(f"Error scraping some fields from {stock_url}")
    return data

# Fetch stock data from Yahoo Finance and calculate returns
def fetch_yfinance_data(ticker):
    stock_data = yf.Ticker(ticker).history(period="5y")
    stock_data['6_month_return'] = stock_data['Close'].pct_change(126)
    stock_data['1_year_return'] = stock_data['Close'].pct_change(252)
    stock_data['5_year_return'] = stock_data['Close'].pct_change(1260)
    return stock_data

# Collect all stock data
all_stock_data = []

for stock in stocks:
    # Scrape data from Screener.in
    screener_data = scrape_screener(stock['url'])
    
    # Fetch OHLCV data and calculate returns
    stock_data_yf = fetch_yfinance_data(stock['ticker'])
    
    # Combine data into a DataFrame
    latest_data = {
        "Ticker": stock['ticker'],
        "PE": screener_data.get('PE', None),
        "EPS": screener_data.get('EPS', None),
        "52_Week_High": screener_data.get('52_Week_High', None),
        "52_Week_Low": screener_data.get('52_Week_Low', None),
        "Market_Cap": screener_data.get('Market_Cap', None),
        "6_month_return": stock_data_yf['6_month_return'].iloc[-1] if not stock_data_yf['6_month_return'].empty else None,
        "1_year_return": stock_data_yf['1_year_return'].iloc[-1] if not stock_data_yf['1_year_return'].empty else None,
        "5_year_return": stock_data_yf['5_year_return'].iloc[-1] if not stock_data_yf['5_year_return'].empty else None,
    }
    all_stock_data.append(latest_data)

# Create DataFrame and save as CSV
df = pd.DataFrame(all_stock_data)
csv_path = "Nifty50_Stock_Data.csv"
df.to_csv(csv_path, index=False)

print(f"CSV file generated: {csv_path}")

