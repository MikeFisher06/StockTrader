from flask import Flask, request, jsonify, render_template, url_for, redirect
from polygon import RESTClient
from dotenv import load_dotenv

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

@app.route('/stock/<ticker>')
def get_stock_data(ticker):
    aggs = []
    for a in client.list_aggs(
        ticker,
        1,
        "day",
        "2024-01-01",
        "2024-01-02"
    ):
        aggs.append(a)

    data = [{"time": agg.timestamp, "open": agg.open, "high": agg.high, 
             "low": agg.low, "close": agg.close} for agg in aggs]

    # data = client.get_ticker_details(ticker)
    # return data
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)