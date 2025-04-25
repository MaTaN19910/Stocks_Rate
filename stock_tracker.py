import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import time
import requests
from requests.exceptions import RequestException
import json
import os
from colorama import init, Fore, Style

# Initialize colorama for colored output
init()

def get_stock_data(ticker):
    """
    Fetch the latest stock data for a given ticker
    """
    try:
        # Verify internet connection first
        requests.get('https://finance.yahoo.com', timeout=5)
        
        # Create a Ticker object
        stock = yf.Ticker(ticker)
        
        # Try to get info first to verify the ticker exists
        try:
            info = stock.info
            if not info:
                print(f"Warning: No information available for {ticker}")
                return None
        except Exception as e:
            print(f"Error getting info for {ticker}: {str(e)}")
            return None
            
        # Get the latest data with a longer period
        end_date = datetime.now()
        start_date = end_date - timedelta(days=2)
        
        try:
            data = stock.history(start=start_date, end=end_date)
            if not data.empty and len(data) > 0:
                latest_price = data['Close'].iloc[-1]
                previous_price = data['Close'].iloc[-2] if len(data) > 1 else latest_price
                price_change = latest_price - previous_price
                percent_change = (price_change / previous_price) * 100
                
                return {
                    'ticker': ticker,
                    'price': latest_price,
                    'change': price_change,
                    'percent_change': percent_change,
                    'timestamp': datetime.now().strftime('%H:%M:%S')
                }
            else:
                print(f"Warning: No price data available for {ticker}")
                return None
        except Exception as e:
            print(f"Error fetching history for {ticker}: {str(e)}")
            return None
            
    except RequestException as e:
        print(f"Network error for {ticker}: {str(e)}")
        return None
    except Exception as e:
        print(f"Unexpected error for {ticker}: {str(e)}")
        return None

def main():
    # List of stock tickers to track
    tickers = ['TSLA', 'NVDA', 'GOOGL', 'AMZN', 'PYPL', 'SOFI']
    
    print(f"{Fore.CYAN}Stock Price Tracker - Real Time Updates{Style.RESET_ALL}")
    print(f"{Fore.CYAN}===================================={Style.RESET_ALL}")
    
    # Store previous prices for comparison
    previous_prices = {ticker: None for ticker in tickers}
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen
        
        print(f"\n{Fore.YELLOW}Fetching latest stock prices...{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'Ticker':<8} {'Price':<12} {'Change':<12} {'% Change':<12} {'Time'}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'-' * 50}{Style.RESET_ALL}")
        
        for ticker in tickers:
            data = get_stock_data(ticker)
            if data:
                # Determine color based on price change
                color = Fore.GREEN if data['change'] >= 0 else Fore.RED
                
                # Format the change and percent change
                change_str = f"{data['change']:+.2f}"
                percent_str = f"{data['percent_change']:+.2f}%"
                
                print(f"{ticker:<8} {color}${data['price']:<11.2f} {change_str:<12} {percent_str:<12} {data['timestamp']}{Style.RESET_ALL}")
                
                # Update previous price
                previous_prices[ticker] = data['price']
        
        # Wait for 5 seconds before next update
        time.sleep(5)

if __name__ == "__main__":
    main() 