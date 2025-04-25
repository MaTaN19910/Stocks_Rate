import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import time
import requests
from requests.exceptions import RequestException
import json
import os
from colorama import init, Fore, Style
import csv

# Initialize colorama for colored output
init()

def load_portfolio():
    """Load portfolio data from JSON file"""
    try:
        with open('portfolio.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"{Fore.RED}Error: portfolio.json not found. Please create your portfolio first.{Style.RESET_ALL}")
        return None
    except json.JSONDecodeError:
        print(f"{Fore.RED}Error: Invalid JSON format in portfolio.json{Style.RESET_ALL}")
        return None

def get_stock_data(ticker):
    """Fetch the latest stock data for a given ticker"""
    try:
        stock = yf.Ticker(ticker)
        # Get current price and daily data
        data = stock.history(period='2d')  # Get 2 days to calculate daily change
        if data.empty or len(data) < 2:
            return None, None, None, None
            
        current_price = data['Close'].iloc[-1]
        previous_price = data['Close'].iloc[-2]
        daily_change = current_price - previous_price
        daily_change_percent = (daily_change / previous_price) * 100
        
        # Get YTD data
        ytd_data = stock.history(start=datetime(datetime.now().year, 1, 1))
        if ytd_data.empty:
            return current_price, daily_change, daily_change_percent, None
            
        ytd_start_price = ytd_data['Close'].iloc[0]
        ytd_change = ((current_price - ytd_start_price) / ytd_start_price) * 100
        
        return current_price, daily_change, daily_change_percent, ytd_change
    except Exception as e:
        print(f"Error fetching data for {ticker}: {str(e)}")
        return None, None, None, None

def calculate_portfolio_performance(portfolio):
    """Calculate portfolio performance"""
    if not portfolio:
        return None

    total_investment = 0
    total_current_value = 0
    total_ytd_investment = 0
    total_daily_change = 0
    performance_data = []

    for investment in portfolio['investments']:
        ticker = investment['ticker']
        shares = investment['shares']
        purchase_price = investment['purchase_price']
        current_price, daily_change, daily_change_percent, ytd_change = get_stock_data(ticker)

        if current_price is not None:
            investment_value = shares * purchase_price
            current_value = shares * current_price
            gain_loss = current_value - investment_value
            gain_loss_percent = (gain_loss / investment_value) * 100

            # Calculate daily change in value
            daily_value_change = shares * daily_change if daily_change is not None else 0
            total_daily_change += daily_value_change

            # Calculate YTD value
            ytd_start_value = current_value / (1 + (ytd_change/100)) if ytd_change is not None else None
            ytd_gain_loss = current_value - ytd_start_value if ytd_start_value is not None else None

            total_investment += investment_value
            total_current_value += current_value
            if ytd_start_value is not None:
                total_ytd_investment += ytd_start_value

            performance_data.append({
                'ticker': ticker,
                'shares': shares,
                'purchase_price': purchase_price,
                'current_price': current_price,
                'investment_value': investment_value,
                'current_value': current_value,
                'gain_loss': gain_loss,
                'gain_loss_percent': gain_loss_percent,
                'daily_change': daily_change,
                'daily_change_percent': daily_change_percent,
                'daily_value_change': daily_value_change,
                'ytd_change': ytd_change,
                'ytd_gain_loss': ytd_gain_loss
            })

    if performance_data:
        total_gain_loss = total_current_value - total_investment
        total_gain_loss_percent = (total_gain_loss / total_investment) * 100
        
        # Calculate total YTD performance
        total_ytd_gain_loss = total_current_value - total_ytd_investment if total_ytd_investment > 0 else None
        total_ytd_percent = ((total_current_value - total_ytd_investment) / total_ytd_investment * 100) if total_ytd_investment > 0 else None

        # Calculate total daily change percentage
        total_daily_change_percent = (total_daily_change / (total_current_value - total_daily_change)) * 100 if total_current_value > 0 else 0

        return {
            'performance_data': performance_data,
            'total_investment': total_investment,
            'total_current_value': total_current_value,
            'total_gain_loss': total_gain_loss,
            'total_gain_loss_percent': total_gain_loss_percent,
            'total_ytd_investment': total_ytd_investment,
            'total_ytd_gain_loss': total_ytd_gain_loss,
            'total_ytd_percent': total_ytd_percent,
            'total_daily_change': total_daily_change,
            'total_daily_change_percent': total_daily_change_percent
        }
    return None

def display_portfolio_performance(performance):
    """Display portfolio performance in a formatted way"""
    if not performance:
        return

    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(f"\n{Fore.CYAN}Portfolio Performance Tracker{Style.RESET_ALL}")
    print(f"{Fore.CYAN}==========================={Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}\n")
    
    # Display individual investments
    print(f"{Fore.CYAN}{'Stock':<8} {'Shares':<8} {'Current':<12} {'Daily $':<12} {'Daily %':<12} {'Value':<12} {'Gain/Loss':<12} {'YTD %'}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'-' * 100}{Style.RESET_ALL}")
    
    for data in performance['performance_data']:
        color = Fore.GREEN if data['gain_loss'] >= 0 else Fore.RED
        daily_color = Fore.GREEN if data['daily_change'] is None or data['daily_change'] >= 0 else Fore.RED
        ytd_color = Fore.GREEN if data['ytd_change'] is None or data['ytd_change'] >= 0 else Fore.RED
        
        daily_str = f"${data['daily_value_change']:+.2f}" if data['daily_change'] is not None else "N/A"
        daily_percent_str = f"{data['daily_change_percent']:+.2f}%" if data['daily_change_percent'] is not None else "N/A"
        ytd_str = f"{data['ytd_change']:+.2f}%" if data['ytd_change'] is not None else "N/A"
        
        print(f"{data['ticker']:<8} {data['shares']:<8} "
              f"${data['current_price']:<11.2f} {daily_color}{daily_str:<12} {daily_percent_str:<12}{Style.RESET_ALL} "
              f"${data['current_value']:<11.2f} {color}${data['gain_loss']:<11.2f} "
              f"{ytd_color}{ytd_str}{Style.RESET_ALL}")
    
    # Display total portfolio performance
    print(f"\n{Fore.CYAN}{'Total Portfolio Summary':<100}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'-' * 100}{Style.RESET_ALL}")
    total_color = Fore.GREEN if performance['total_gain_loss'] >= 0 else Fore.RED
    daily_total_color = Fore.GREEN if performance['total_daily_change'] >= 0 else Fore.RED
    ytd_total_color = Fore.GREEN if performance['total_ytd_percent'] is None or performance['total_ytd_percent'] >= 0 else Fore.RED
    
    print(f"{'Total Investment:':<20} ${performance['total_investment']:.2f}")
    print(f"{'Current Value:':<20} ${performance['total_current_value']:.2f}")
    print(f"{'Daily Change:':<20} {daily_total_color}${performance['total_daily_change']:+.2f} "
          f"({performance['total_daily_change_percent']:+.2f}%){Style.RESET_ALL}")
    print(f"{'Total Gain/Loss:':<20} {total_color}${performance['total_gain_loss']:.2f} "
          f"({performance['total_gain_loss_percent']:+.2f}%){Style.RESET_ALL}")
    print(f"{'YTD Performance:':<20} {ytd_total_color}${performance['total_ytd_gain_loss']:.2f} "
          f"({performance['total_ytd_percent']:+.2f}%){Style.RESET_ALL}")

def save_portfolio_to_csv(performance, filename="portfolio_data.csv"):
    """Save portfolio performance data to a CSV file"""
    try:
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write header
            writer.writerow(['Stock', 'Shares', 'Current Price', 'Daily $', 'Daily %', 
                           'Current Value', 'Gain/Loss', '% Change', 'YTD %'])
            
            # Write individual stock data
            for data in performance['performance_data']:
                daily_str = f"${data['daily_value_change']:+.2f}" if data['daily_change'] is not None else "N/A"
                daily_percent_str = f"{data['daily_change_percent']:+.2f}%" if data['daily_change_percent'] is not None else "N/A"
                ytd_str = f"{data['ytd_change']:+.2f}%" if data['ytd_change'] is not None else "N/A"
                
                writer.writerow([
                    data['ticker'],
                    data['shares'],
                    f"${data['current_price']:.2f}",
                    daily_str,
                    daily_percent_str,
                    f"${data['current_value']:.2f}",
                    f"${data['gain_loss']:+.2f}",
                    f"{data['gain_loss_percent']:+.2f}%",
                    ytd_str
                ])
            
            # Write summary data
            writer.writerow([])  # Empty row for separation
            writer.writerow(['Portfolio Summary'])
            writer.writerow(['Total Investment:', f"${performance['total_investment']:.2f}"])
            writer.writerow(['Current Value:', f"${performance['total_current_value']:.2f}"])
            writer.writerow(['Daily Change:', f"${performance['total_daily_change']:+.2f}",
                           f"({performance['total_daily_change_percent']:+.2f}%)"])
            writer.writerow(['Total Gain/Loss:', f"${performance['total_gain_loss']:+.2f}",
                           f"({performance['total_gain_loss_percent']:+.2f}%)"])
            writer.writerow(['YTD Performance:', f"${performance['total_ytd_gain_loss']:+.2f}",
                           f"({performance['total_ytd_percent']:+.2f}%)"])
            
            # Write timestamp
            writer.writerow([])
            writer.writerow(['Last Updated:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
            
        print(f"\n{Fore.GREEN}Portfolio data saved to {filename}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error saving portfolio data: {str(e)}{Style.RESET_ALL}")

def main():
    portfolio = load_portfolio()
    if not portfolio:
        return

    while True:
        performance = calculate_portfolio_performance(portfolio)
        if performance:
            display_portfolio_performance(performance)
            save_portfolio_to_csv(performance)  # Save data to CSV
        time.sleep(5)  # Update every 5 seconds

if __name__ == "__main__":
    main() 