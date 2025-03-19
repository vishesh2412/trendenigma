# TrendEnigma

TrendEnigma is a Flask-based stock price prediction web application that uses historical stock data to predict future closing prices using a machine learning model.

## Features

- Fetches real-time stock data using **Alpha Vantage API**.
- Supports **multiple stock tickers** (AAPL, MSFT, GOOGL, RELIANCE.NS, TCS.NS, etc.).
- Implements **Linear Regression** for stock price prediction.
- Displays sidebar stock prices for quick reference.
- Provides a simple and responsive UI.

## Installation

Clone the repository:
git clone https://github.com/yourusername/TrendEnigma.git
cd TrendEnigma

Create a virtual environment:
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

Install dependencies:
pip install -r requirements.txt

Run the Flask app:
python app.py

Open a web browser and visit:
http://127.0.0.1:5000/


File Structure
TrendEnigma/
│── app.py               # Main Flask application
│── stock_model.py       # Stock data fetching & prediction model
│── templates/           # HTML templates
│   ├── home.html
│   ├── index.html
│   ├── result.html
│── requirements.txt     # Python dependencies


Usage
Home Page (/): Welcome page with a "Get Started" button.
Stock Prediction Page (/index): Enter a stock ticker (e.g., AAPL, RELIANCE.NS).
Prediction Result (/predict): Displays today's and predicted closing price.
Technologies Used
Flask (Web Framework)
yFinance (Stock Data Fetching)
Pandas (Data Processing)
Scikit-Learn (Machine Learning)
HTML, CSS (Frontend)
Screenshots
Home Page

Prediction Page

Result Page

License
This project is open-source and available under the MIT License.
