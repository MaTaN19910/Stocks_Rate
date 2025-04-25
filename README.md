# Portfolio Tracker

A real-time stock portfolio tracker that displays your investments, daily performance, and YTD changes. The application includes both a console interface and a web interface for easy monitoring.

## Features

- Real-time stock price tracking
- Portfolio performance monitoring
- Daily gain/loss tracking
- Year-to-Date (YTD) performance
- Web interface for remote monitoring
- CSV export functionality
- Color-coded performance indicators

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/portfolio-tracker.git
cd portfolio-tracker
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Configuration

1. Edit the `portfolio.json` file with your investments:
```json
{
    "investments": [
        {
            "ticker": "STOCK_SYMBOL",
            "shares": NUMBER_OF_SHARES,
            "purchase_price": PURCHASE_PRICE,
            "purchase_date": "YYYY-MM-DD"
        }
    ]
}
```

## Usage

### Console Interface
Run the portfolio tracker:
```bash
python portfolio_tracker.py
```

### Web Interface
Start the web server:
```bash
python portfolio_web.py
```
Then open your web browser and navigate to the displayed URL (typically http://your-ip:5000)

## Features

- Real-time updates (every 5 seconds)
- Color-coded performance indicators
- Daily and YTD performance tracking
- Web interface for remote monitoring
- CSV export functionality
- Portfolio summary with total gains/losses

## File Structure

- `portfolio_tracker.py` - Main portfolio tracking application
- `portfolio_web.py` - Web interface for remote monitoring
- `portfolio.json` - Your investment portfolio configuration
- `portfolio_data.csv` - Generated portfolio performance data
- `requirements.txt` - Python package dependencies

## License

MIT License

## Contributing

Feel free to submit issues and enhancement requests!