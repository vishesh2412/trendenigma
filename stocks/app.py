from flask import Flask, render_template, request
from stock_model import fetch_stock_data, fetch_historical_data, prepare_data, train_model, get_next_trading_day
import time

app = Flask(__name__)

def get_sidebar_stock_data():
    """Fetch real-time stock data for the sidebar."""
    tickers = ["AAPL", "MSFT", "GOOGL", "RELIANCE.BSE", "TCS.BSE"]
    stock_data = {}
    for ticker in tickers:
        data = fetch_stock_data(ticker)
        if data:
            stock_data[ticker] = f"${data['price']:.2f}" if "." not in ticker else f"₹{data['price']:.2f}"
        else:
            stock_data[ticker] = "N/A"
        time.sleep(12)  # Respect API rate limits
    return stock_data

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/index')
def index():
    try:
        stock_data = get_sidebar_stock_data()
        return render_template('index.html', stock_data=stock_data)
    except Exception as e:
        print(f"Error in index route: {str(e)}")
        default_data = {ticker: "N/A" for ticker in ["AAPL", "MSFT", "GOOGL", "RELIANCE.BSE", "TCS.BSE"]}
        return render_template('index.html', stock_data=default_data)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        ticker = request.form['ticker'].strip().upper()
        
        # Handle Indian stocks
        if ticker in ["RELIANCE", "TCS", "INFY"] and "." not in ticker:
            ticker += ".BSE"
        
        # Fetch data
        data = fetch_historical_data(ticker)
        if data.empty:
            raise ValueError("No historical data available")
        
        # Prepare and train model
        X, y = prepare_data(data)
        if len(X) < 5:
            raise ValueError("Not enough data points for prediction")
            
        model = train_model(X, y)
        
        # Make prediction
        last_day = X[-1][0] + 1
        prediction = model.predict([[last_day]])[0]
        
        # Get current price
        current_data = fetch_stock_data(ticker)
        current_price = current_data['price'] if current_data else data.iloc[-1]["Close"]
        
        return render_template('result.html', 
                            ticker=ticker,
                            today_price=round(float(current_price), 2),
                            prediction=round(float(prediction), 2),
                            stock_data=get_sidebar_stock_data())
        
    except Exception as e:
        print(f"Prediction error: {str(e)}")
        return render_template('result.html',
                            ticker=ticker,
                            prediction=f"Error: {str(e)}",
                            stock_data=get_sidebar_stock_data())

if __name__ == '__main__':
    app.run(debug=True)
