import io
import logging
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from django.http import JsonResponse, HttpResponse, FileResponse
from django.shortcuts import render

logging.basicConfig(level=logging.INFO)

def home_view(request):
    return render(request, 'stock_app/home.html')

def fetch_stock_data(ticker: str, start_date: str, end_date: str, interval: str = '1d'):
    logging.info(f"Fetching data for {ticker} from {start_date} to {end_date} with interval {interval}...")
    stock = yf.download(ticker, start=start_date, end=end_date, interval=interval, auto_adjust=False)
    if stock.empty:
        logging.warning(f"No data retrieved for {ticker}. Check ticker symbol or date range.")
        return stock
    logging.info("Data successfully retrieved.")
    # Flatten MultiIndex columns if present
    if isinstance(stock.columns, pd.MultiIndex):
        stock.columns = stock.columns.get_level_values(0)
    return stock

def moving_average_crossover_strategy(data, short_window=10, long_window=20):
    if data.empty or "Close" not in data.columns:
        logging.error("Data does not contain 'Close' column.")
        return data
    data['SMA_Short'] = data['Close'].rolling(window=short_window).mean()
    data['SMA_Long'] = data['Close'].rolling(window=long_window).mean()
    data['Signal'] = 0
    data.loc[data['SMA_Short'] > data['SMA_Long'], 'Signal'] = 1
    data.loc[data['SMA_Short'] < data['SMA_Long'], 'Signal'] = -1
    return data

def backtest_strategy(data, initial_balance=10000):
    if data.empty or "Close" not in data.columns:
        logging.error("Data does not contain 'Close' column.")
        return data
    balance = initial_balance
    position = 0
    data['Portfolio Value'] = balance
    for i in range(1, len(data)):
        if data['Signal'].iloc[i-1] == 1 and position == 0:
            position = balance / data['Close'].iloc[i]
            balance = 0
        elif data['Signal'].iloc[i-1] == -1 and position > 0:
            balance = position * data['Close'].iloc[i]
            position = 0
        data.at[data.index[i], 'Portfolio Value'] = balance + (position * data['Close'].iloc[i])
    return data

def stock_view(request):
    ticker = request.GET.get('ticker', 'AAPL')
    start_date = request.GET.get('start_date', '2024-01-01')
    end_date = request.GET.get('end_date', '2024-02-17')
    interval = request.GET.get('interval', '1d')
    data = fetch_stock_data(ticker, start_date, end_date, interval)
    if data.empty:
        return JsonResponse({"error": "No data retrieved. Check ticker symbol or date range."}, status=400)
    data_json = data.reset_index().to_dict(orient='records')
    return JsonResponse(data_json, safe=False)

def analysis_view(request):
    ticker = request.GET.get('ticker', 'AAPL')
    start_date = request.GET.get('start_date', '2024-01-01')
    end_date = request.GET.get('end_date', '2024-02-17')
    interval = request.GET.get('interval', '1d')
    data = fetch_stock_data(ticker, start_date, end_date, interval)
    if data.empty:
        return JsonResponse({"error": "No data retrieved. Check ticker symbol or date range."}, status=400)
    data = moving_average_crossover_strategy(data)
    data = backtest_strategy(data)
    # Replace NaN/Inf with None to allow safe JSON serialization
    data = data.replace([np.nan, np.inf, -np.inf], None)
    data_json = data.reset_index().to_dict(orient='records')
    return JsonResponse(data_json, safe=False)

def generate_stock_plot(data, ticker: str):
    plt.figure(figsize=(10, 6))
    plt.plot(data.index, data['Close'], label='Close Price', color='blue')
    if 'SMA_Short' in data.columns:
        plt.plot(data.index, data['SMA_Short'], label='SMA Short', color='orange')
    if 'SMA_Long' in data.columns:
        plt.plot(data.index, data['SMA_Long'], label='SMA Long', color='green')
    plt.title(f"{ticker} Stock Price and Moving Averages")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    return buf

def plot_view(request):
    ticker = request.GET.get('ticker', 'AAPL')
    start_date = request.GET.get('start_date', '2024-01-01')
    end_date = request.GET.get('end_date', '2024-02-17')
    interval = request.GET.get('interval', '1d')
    data = fetch_stock_data(ticker, start_date, end_date, interval)
    if data.empty:
        return JsonResponse({"error": "No data retrieved. Check ticker symbol or date range."}, status=400)
    data = moving_average_crossover_strategy(data)
    buf = generate_stock_plot(data, ticker)
    return FileResponse(buf, content_type='image/png')

def news_view(request):
    ticker = request.GET.get('ticker', 'AAPL')
    news = [
        {"title": f"Latest news for {ticker} - Market Update", "date": "2024-01-15", "summary": "Summary of market movements."},
        {"title": f"{ticker} Announces Quarterly Earnings", "date": "2024-01-25", "summary": "Earnings results beat expectations."}
    ]
    return JsonResponse(news, safe=False)
