import os
from glob import glob
from datetime import date
import pandas as pd

# Custom functions
from alert_server import AlertServer
from moving_averages import moving_averages
from efficient_frontier import plot_efficient_frontier

# Prepare images directory
if not os.path.exists('images'):
    os.mkdir('images')

for file in glob('images/*'):
    os.remove(file)

# Specify what stocks to track
portfolio_qty = pd.DataFrame.from_dict({'BPTRX': 1, 'DAL': 1, 'ETHE': 1, 'FXAIX': 1, 'GOOGL': 1, 'IXUS': 1, 'LIT': 1, 'NVDA': 1, 'UAL': 1, 'URNM': 1, 'VIOG': 1, 'VOO': 1}, orient='index').transpose()

# Add 0 weight tickers from S&P 500
portfolio_tickers = portfolio_qty.columns.tolist()
sp500_tickers = pd.read_csv('sandp500Stocks.csv')['Symbol']
for ticker in sp500_tickers:
    if ticker not in portfolio_tickers:
        portfolio_qty[ticker] = 0

# Create final ticker list
tickers = portfolio_qty.columns.tolist()

# Run moving averages
buy_list, sell_list = moving_averages(tickers)
print(f'Buy_list:\n{buy_list}\nSell_list:\n{sell_list}')

# Run Efficient Frontier
plot_efficient_frontier(portfolio_qty)

# Send Alert
alert = AlertServer()
alert.send_email(f'Stock Update: {date.today()}', f'Good Morning! Heres your daily stock update.', images=list(glob('images/*')))
