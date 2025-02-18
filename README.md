# Basic Stock Trading Dashboard for Dilution Tracker

This project is a stock trading dashboard built using Django. It was developed specifically as part of my application for the **Full Stack Software Engineer Intern** position at **Dilution Tracker**. The project demonstrates full-stack development skills by integrating financial data retrieval, analysis, backtesting, and visualization into a modern web application.

## Overview

The Stock Trading Dashboard allows users to:
- **Fetch Stock Data:** Retrieve historical stock data using the [yfinance](https://pypi.org/project/yfinance/) library.
- **Perform Analysis:** Calculate short-term and long-term simple moving averages (SMA), generate buy/sell signals, and backtest a basic trading strategy. (using numpy)
- **Visualize Data:** Display a plot of the stock’s closing price along with calculated moving averages using Matplotlib.
- **View Financial News:** Show stubbed financial news items related to the stock.

## Features

- **Data Retrieval:** Uses yfinance to download stock data from Yahoo Finance.
- **Moving Average Strategy:** Calculates SMA values for specified window sizes and generates trading signals.
- **Backtesting:** Simulates a trading strategy to calculate portfolio value over time.
- **Plotting:** Generates a chart of the stock's price and its moving averages.
- **REST API Endpoints:** Provides endpoints to access raw stock data, analysis results, plots, and news.
- **Responsive UI:** A single-page dashboard built with HTML, CSS (Bootstrap), and JavaScript (Fetch API) that integrates with the backend API.

## Technologies Used

- **Backend:** Python, Django, yfinance, Pandas, NumPy, Matplotlib
- **Frontend:** HTML, CSS (Bootstrap), JavaScript (Fetch API)
- **Version Control:** Git

## Setup Instructions

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/Deva-101/Dilution-Tracker.git
   cd stock_project

2. **Create a Virtual Environment and Install Dependencies:**

   ```bash
   python -m venv venv
   venv\Scripts\activate  # For Mac: source venv/bin/activate
   pip install -r requirements.txt

3. **Apply Migrations:**

   ```bash
   python manage.py migrate

4. **Run the Development Server:**

   ```bash
   python manage.py runserver


5. **Access the Application:**

   Open your browser and navigate to http://127.0.0.1:8000/
