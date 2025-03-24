import requests
import pandas as pd
import time
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from datetime import datetime, timedelta

# Replace with your Alpha Vantage API key
API_KEY = "alpha_vantage+api_key_here"

def fetch_stock_data(ticker):
    """Fetch real-time stock data using Alpha Vantage."""
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        
        if "Global Quote" not in data:
            print(f"Error fetching data for {ticker}: {data}")
            return None
        
        quote = data["Global Quote"]
        return {
            'symbol': quote.get('01. symbol', ticker),
            'price': float(quote.get('05. price', 0)),
            'change': float(quote.get('09. change', 0)),
            'change_percent': quote.get('10. change percent', '0%')
        }
    except Exception as e:
        print(f"Error fetching {ticker}: {str(e)}")
        return None

def fetch_historical_data(ticker):
    """Fetch historical stock data for prediction."""
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&outputsize=compact&apikey={API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        
        if "Time Series (Daily)" not in data:
            print(f"Error fetching historical data: {data}")
            return pd.DataFrame()
        
        df = pd.DataFrame(data["Time Series (Daily)"]).T
        df.index = pd.to_datetime(df.index)
        df = df.astype(float)
        df.columns = ["Open", "High", "Low", "Close", "Volume"]
        return df.sort_index()
    except Exception as e:
        print(f"Error fetching historical data: {str(e)}")
        return pd.DataFrame()

def prepare_data(data):
    """Prepare data for training."""
    data['Days'] = (data.index - data.index.min()).days
    X = data[['Days']].values
    y = data['Close'].values
    return X, y

def train_model(X, y):
    """Train a Linear Regression model."""
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
    while next_day.weekday() >= 5:
        next_day += timedelta(days=1)
    return next_day
