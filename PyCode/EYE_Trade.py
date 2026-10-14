import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import sys

def plot_stock_price(ticker):
    """Fetches historical stock data and plots the closing price."""
    try:
        # Download data for the last year
        stock_data = yf.download(ticker, period="1y")

        if stock_data.empty:
            print(f"Could not fetch data for ticker: {ticker}. Please check the ticker symbol.")
            return

        # Plot the 'Close' price
        plt.figure(figsize=(12, 6))
        plt.plot(stock_data['Close'])
        plt.title(f'{ticker} Stock Price (Last Year)')
        plt.xlabel('Date')
        plt.ylabel('Closing Price')
        plt.grid(True)
        plt.show()

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please ensure the ticker symbol is correct and you have an internet connection.")

if __name__ == "__main__":
    # Ask the user for the stock ticker symbol
    stock_code = input("Enter the stock ticker symbol (e.g., AAPL, GOOGL, MSFT): ").upper()

    # Call the function to fetch data and plot
    plot_stock_price(stock_code)
