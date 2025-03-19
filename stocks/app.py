from flask import Flask, render_template, request, redirect, url_for
from stock_model import fetch_stock_data, prepare_data, train_model, get_next_trading_day
from datetime import datetime, timedelta

app = Flask(__name__)

def get_sidebar_stock_data():
    """Fetch real-time stock data for the sidebar."""
    tickers = ["AAPL", "MSFT", "GOOGL", "RELIANCE.NS", "TCS.NS"]
    stock_data = {}
    for ticker in tickers:
        data = fetch_stock_data(ticker)
        if not data.empty:
            stock_data[ticker] = round(data.iloc[-1]["Close"], 2)
        else:
            stock_data[ticker] = "N/A"
    return stock_data

@app.route('/')
def home():
    """Render the home page."""
    return render_template('home.html')

@app.route('/index')
def index():
    """Render the main page with stock predictions."""
    stock_data = get_sidebar_stock_data()
    return render_template('index.html', stock_data=stock_data)

@app.route('/predict', methods=['POST'])
def predict():
    # Get user input from the form
    ticker = request.form['ticker'].strip().upper()
    
    # Fetch stock data
    data = fetch_stock_data(ticker)
    if data.empty:
        stock_data = get_sidebar_stock_data()
        return render_template('result.html', ticker=ticker, prediction="No data available for the given ticker.", stock_data=stock_data)
    
    # Prepare data
    X, y = prepare_data(data)
    
    # Check if the dataset is too small
    if len(X) < 5:
        stock_data = get_sidebar_stock_data()
        return render_template('result.html', ticker=ticker, prediction="Not enough data to make a prediction.", stock_data=stock_data)
    
    # Train the model
    model = train_model(X, y)
    
    # Get the last available date in the data
    last_date = data.index[-1]
    
    # Calculate the next trading day
    next_trading_day = get_next_trading_day(last_date)
    
    # Calculate the number of days for the next trading day
    days_since_start = (next_trading_day - data.index.min()).days
    
    # Predict the next trading day's closing price
    prediction = model.predict([[days_since_start]])
    
    # Round the prediction value
    prediction_rounded = round(float(prediction[0]), 2)
    
    # Get today's closing price (if available)
    today_price = data.iloc[-1]["Close"] if len(data) > 0 else "N/A"
    
    # Fetch sidebar stock data
    stock_data = get_sidebar_stock_data()
    
    # Render the result template with the prediction
    return render_template('result.html', ticker=ticker, today_price=today_price, prediction=prediction_rounded, stock_data=stock_data)

if __name__ == '__main__':
    app.run(debug=True)