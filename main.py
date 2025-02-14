from flask import Flask, request, jsonify, render_template, url_for, redirect
from polygon import RESTClient
from dotenv import load_dotenv
from datetime import date, timedelta

import os
import requests
import json

app = Flask(__name__)
app.secret_key = 'SECRET KEY'

load_dotenv()

POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")

client = RESTClient(POLYGON_API_KEY)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'user' or request.form['password'] != 'pwd':
            error = 'Invalid login. Please try again.'
        else:
            return redirect(url_for('index'))

    return render_template('login.html', error=error)

@app.route('/watchlist')
def watchlist():
    return render_template('watchlist.html')

@app.route('/stock', methods=['POST'])
def get_stock_data():
    if request.method == 'POST':
        ticker = request.form['ticker']
        ticker = ticker.upper()
        # Get dates for yesterday and today
        today = date.today()
        yesterday = today - timedelta(days=1)

        aggs = client.get_aggs(
            ticker,
            1,
            "day",
            yesterday,
            today)
        data = aggs[0]
        return render_template('stock.html', open=data.open, close=data.close, high=data.high, low=data.low)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)