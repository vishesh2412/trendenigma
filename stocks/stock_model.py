import requests
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from datetime import datetime, timedelta

# Replace with your Alpha Vantage API key
API_KEY = "YOUR_ALPHA_VANTAGE_API_KEY"

def fetch_stock_data(ticker):
    """Fetch real-time and historical stock data using Alpha Vantage."""
    # Handle Indian tickers (add .NS or .BO suffix if missing)
    if "." not in ticker:
        ticker += ".NS"  # Default to NSE for Indian companies
    
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    if "Time Series (Daily)" not in data:
        print(f"Error fetching data: {data}")
        return pd.DataFrame()
    
    # Convert JSON data to DataFrame
    stock_data = pd.DataFrame(data["Time Series (Daily)"]).T
    stock_data.index = pd.to_datetime(stock_data.index)
    stock_data = stock_data.astype(float)
    stock_data.columns = ["Open", "High", "Low", "Close", "Volume"]
    return stock_data

def prepare_data(data):
    """Prepare data for training."""
    data['Days'] = (data.index - data.index.min()).days
    X = data[['Days']].values  # Convert to 2D array
    y = data['Close'].values   # Convert to 1D array
    return X, y

def train_model(X, y):
    """Train a Linear Regression model."""
    if len(X) < 5:
        raise ValueError("Not enough data to train the model.")
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    print(f"Mean Squared Error: {mse}")
    return model

def get_next_trading_day(last_date):
    """Get the next trading day (skip weekends)."""
    next_day = last_date + timedelta(days=1)
    while next_day.weekday() >= 5:  # 5 = Saturday, 6 = Sunday
        next_day += timedelta(days=1)
    return next_day